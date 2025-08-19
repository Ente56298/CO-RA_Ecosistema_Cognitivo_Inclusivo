#!/usr/bin/env node
/**
 * TenancingoLive Web Server
 * Sistema de streaming con autenticación por tokens y pagos
 */

import express from 'express';
import jwt from 'jsonwebtoken';
import cors from 'cors';
import helmet from 'helmet';
import rateLimit from 'express-rate-limit';
import { readFileSync } from 'fs';
import { parse } from 'yaml';
import path from 'path';

const app = express();
const PORT = process.env.PORT || 8080;
const JWT_SECRET = process.env.JWT_SECRET || 'change_me_in_production';

// Middleware de seguridad
app.use(helmet());
app.use(cors());
app.use(express.json());
app.use(express.static('public'));

// Rate limiting
const limiter = rateLimit({
    windowMs: 15 * 60 * 1000, // 15 minutos
    max: 100 // máximo 100 requests por IP
});
app.use(limiter);

// Almacén en memoria (usar Redis en producción)
const activeStreams = new Map();
const validTokens = new Set();

/**
 * Autenticación de stream (llamado por NGINX)
 */
app.post('/auth/stream', (req, res) => {
    const streamKey = req.body.name || req.query.key;
    
    console.log(`🔐 Autenticación de stream: ${streamKey}`);
    
    // Verificar si el stream key es válido
    const event = getEventByStreamKey(streamKey);
    
    if (event) {
        activeStreams.set(streamKey, {
            eventId: event.id,
            startTime: new Date(),
            viewers: 0
        });
        
        console.log(`✅ Stream autorizado: ${event.titulo}`);
        res.status(200).send('OK');
    } else {
        console.log(`❌ Stream key inválido: ${streamKey}`);
        res.status(403).send('Forbidden');
    }
});

/**
 * Webhook de pago completado
 */
app.post('/webhook/pago', (req, res) => {
    const { email, eventId, paymentId } = req.body;
    
    console.log(`💰 Pago recibido: ${email} para evento ${eventId}`);
    
    try {
        // Generar token de acceso
        const token = jwt.sign(
            { 
                email, 
                eventId, 
                paymentId,
                type: 'access' 
            }, 
            JWT_SECRET, 
            { expiresIn: '6h' }
        );
        
        // Guardar token válido
        validTokens.add(token);
        
        // Generar link de acceso
        const accessLink = `${req.protocol}://${req.get('host')}/watch/${eventId}?t=${token}`;
        
        // TODO: Enviar email con el link
        console.log(`📧 Link de acceso generado: ${accessLink}`);
        
        res.json({ 
            ok: true, 
            link: accessLink,
            token: token
        });
        
    } catch (error) {
        console.error('Error procesando pago:', error);
        res.status(500).json({ error: 'Error interno' });
    }
});

/**
 * Página de visualización del evento
 */
app.get('/watch/:eventId', (req, res) => {
    const { eventId } = req.params;
    const { t: token } = req.query;
    
    if (!token) {
        return res.status(401).send(`
            <h1>🔒 Acceso Requerido</h1>
            <p>Necesitas un token válido para ver este evento.</p>
            <a href="/events/${eventId}">Comprar acceso</a>
        `);
    }
    
    try {
        // Verificar token
        const decoded = jwt.verify(token, JWT_SECRET);
        
        if (decoded.eventId !== eventId || !validTokens.has(token)) {
            throw new Error('Token inválido');
        }
        
        // Obtener información del evento
        const event = getEventById(eventId);
        
        if (!event) {
            return res.status(404).send('<h1>❌ Evento no encontrado</h1>');
        }
        
        // Servir página de visualización
        const watchPage = generateWatchPage(event, decoded);
        res.send(watchPage);
        
    } catch (error) {
        console.log(`❌ Token inválido para evento ${eventId}: ${error.message}`);
        res.status(401).send(`
            <h1>🚫 Acceso Denegado</h1>
            <p>Token inválido o expirado.</p>
            <a href="/events/${eventId}">Comprar nuevo acceso</a>
        `);
    }
});

/**
 * Landing page del evento
 */
app.get('/events/:eventId', (req, res) => {
    const { eventId } = req.params;
    const event = getEventById(eventId);
    
    if (!event) {
        return res.status(404).send('<h1>❌ Evento no encontrado</h1>');
    }
    
    const landingPage = generateLandingPage(event);
    res.send(landingPage);
});

/**
 * API: Estado de streams activos
 */
app.get('/api/streams', (req, res) => {
    const streams = Array.from(activeStreams.entries()).map(([key, data]) => ({
        streamKey: key,
        eventId: data.eventId,
        startTime: data.startTime,
        viewers: data.viewers,
        duration: Math.floor((Date.now() - data.startTime.getTime()) / 1000)
    }));
    
    res.json({ streams });
});

/**
 * Webhook: Notificación de reproducción
 */
app.post('/webhook/play', (req, res) => {
    const streamKey = req.body.name;
    
    if (activeStreams.has(streamKey)) {
        const stream = activeStreams.get(streamKey);
        stream.viewers++;
        activeStreams.set(streamKey, stream);
    }
    
    res.status(200).send('OK');
});

// Funciones auxiliares
function getEventById(eventId) {
    try {
        const eventFile = `../events/${eventId}.yml`;
        const eventData = readFileSync(eventFile, 'utf8');
        return parse(eventData);
    } catch (error) {
        return null;
    }
}

function getEventByStreamKey(streamKey) {
    // Buscar evento por stream_key
    // En producción, usar base de datos
    try {
        const events = ['2025-08-22-lucha1']; // Lista de eventos disponibles
        
        for (const eventId of events) {
            const event = getEventById(eventId);
            if (event && event.stream_key === streamKey) {
                return event;
            }
        }
    } catch (error) {
        console.error('Error buscando evento:', error);
    }
    
    return null;
}

function generateWatchPage(event, user) {
    return `
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${event.titulo} - TenancingoLive</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #000; color: #fff; }
        .container { max-width: 1200px; margin: 0 auto; }
        .video-container { position: relative; width: 100%; height: 0; padding-bottom: 56.25%; }
        video { position: absolute; top: 0; left: 0; width: 100%; height: 100%; }
        .info { margin-top: 20px; }
        .user-info { position: absolute; top: 10px; right: 10px; background: rgba(0,0,0,0.7); padding: 10px; border-radius: 5px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎪 ${event.titulo}</h1>
        
        <div class="video-container">
            <video id="player" controls autoplay>
                <source src="/hls/${event.stream_key}.m3u8" type="application/x-mpegURL">
                Tu navegador no soporta HLS
            </video>
        </div>
        
        <div class="info">
            <p><strong>📅 Fecha:</strong> ${new Date(event.inicio).toLocaleString('es-MX')}</p>
            <p><strong>📝 Descripción:</strong> ${event.descripcion}</p>
        </div>
        
        <div class="user-info">
            👤 ${user.email}
        </div>
    </div>
    
    <script src="https://cdn.jsdelivr.net/npm/hls.js@latest"></script>
    <script>
        const video = document.getElementById('player');
        const videoSrc = '/hls/${event.stream_key}.m3u8';
        
        if (Hls.isSupported()) {
            const hls = new Hls();
            hls.loadSource(videoSrc);
            hls.attachMedia(video);
        } else if (video.canPlayType('application/vnd.apple.mpegurl')) {
            video.src = videoSrc;
        }
    </script>
</body>
</html>`;
}

function generateLandingPage(event) {
    return `
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${event.titulo} - TenancingoLive</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: #fff; }
        .container { max-width: 800px; margin: 0 auto; text-align: center; }
        .price { font-size: 3em; font-weight: bold; margin: 20px 0; }
        .buy-button { background: #ff6b6b; color: white; padding: 15px 30px; border: none; border-radius: 5px; font-size: 1.2em; cursor: pointer; }
        .buy-button:hover { background: #ff5252; }
        .info { background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px; margin: 20px 0; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎪 ${event.titulo}</h1>
        
        <div class="info">
            <p><strong>📅 Fecha:</strong> ${new Date(event.inicio).toLocaleString('es-MX')}</p>
            <p><strong>📝 Descripción:</strong> ${event.descripcion}</p>
        </div>
        
        <div class="price">$${event.precio_mxn} MXN</div>
        
        <button class="buy-button" onclick="comprarAcceso()">
            🎫 Comprar Acceso
        </button>
        
        <p><small>Acceso válido por 6 horas desde la compra</small></p>
    </div>
    
    <script>
        function comprarAcceso() {
            // Integrar con Stripe/Conekta/MercadoPago
            alert('Redirigiendo a pasarela de pago...');
            // window.location.href = '/checkout/${event.id}';
        }
    </script>
</body>
</html>`;
}

// Iniciar servidor
app.listen(PORT, () => {
    console.log(`🚀 TenancingoLive Web Server iniciado en puerto ${PORT}`);
    console.log(`📺 RTMP: rtmp://localhost:1935/live`);
    console.log(`🌐 Web: http://localhost:${PORT}`);
    console.log(`📡 HLS: http://localhost:8081/hls/`);
});