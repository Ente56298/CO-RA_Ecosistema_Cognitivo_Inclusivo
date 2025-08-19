<?php
/**
 * Página de visualización con autenticación por token
 * TenancingoLive
 */

require_once 'config/config.php';

$eventId = $_GET['event'] ?? '';
$token = $_GET['token'] ?? '';

if (!$eventId) {
    header('Location: /');
    exit;
}

// Obtener información del evento
$pdo = getDBConnection();
$stmt = $pdo->prepare("SELECT * FROM events WHERE id = ? AND active = 1");
$stmt->execute([$eventId]);
$event = $stmt->fetch();

if (!$event) {
    http_response_code(404);
    echo "<h1>Evento no encontrado</h1>";
    exit;
}

// Verificar token si se proporciona
$hasAccess = false;
$userEmail = '';

if ($token) {
    $tokenData = verifyJWT($token);
    if ($tokenData && $tokenData['event_id'] === $eventId) {
        // Verificar token en base de datos
        $stmt = $pdo->prepare("SELECT * FROM access_tokens WHERE token = ? AND event_id = ? AND expires_at > NOW()");
        $stmt->execute([$token, $eventId]);
        $tokenRecord = $stmt->fetch();
        
        if ($tokenRecord) {
            $hasAccess = true;
            $userEmail = $tokenRecord['email'];
            
            // Log de acceso
            logActivity('stream_access', [
                'event_id' => $eventId,
                'email' => $userEmail,
                'token' => substr($token, 0, 10) . '...'
            ]);
        }
    }
}

// Si no tiene acceso, mostrar página de compra
if (!$hasAccess) {
    ?>
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title><?= htmlspecialchars($event['title']) ?> - TenancingoLive</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; }
            .container { max-width: 800px; margin: 0 auto; text-align: center; }
            .event-card { background: rgba(255,255,255,0.1); padding: 30px; border-radius: 15px; margin: 20px 0; }
            .price { font-size: 3em; font-weight: bold; margin: 20px 0; color: #ffd700; }
            .buy-button { background: #ff6b6b; color: white; padding: 15px 30px; border: none; border-radius: 8px; font-size: 1.2em; cursor: pointer; text-decoration: none; display: inline-block; }
            .buy-button:hover { background: #ff5252; }
            .event-info { text-align: left; margin: 20px 0; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎪 <?= htmlspecialchars($event['title']) ?></h1>
            
            <div class="event-card">
                <div class="event-info">
                    <p><strong>📅 Fecha:</strong> <?= date('d/m/Y H:i', strtotime($event['start_time'])) ?></p>
                    <p><strong>📝 Descripción:</strong> <?= htmlspecialchars($event['description']) ?></p>
                    <p><strong>⏱️ Duración:</strong> <?= $event['duration_minutes'] ?> minutos</p>
                </div>
                
                <div class="price">$<?= number_format($event['price_mxn']) ?> MXN</div>
                
                <a href="checkout.php?event=<?= $eventId ?>" class="buy-button">
                    🎫 Comprar Acceso
                </a>
                
                <p><small>Acceso válido por 6 horas • Pago seguro con Stripe</small></p>
            </div>
            
            <?php if ($event['trailer_url']): ?>
            <div class="event-card">
                <h3>🎬 Vista Previa</h3>
                <video controls style="width: 100%; max-width: 600px;">
                    <source src="<?= htmlspecialchars($event['trailer_url']) ?>" type="video/mp4">
                </video>
            </div>
            <?php endif; ?>
        </div>
    </body>
    </html>
    <?php
    exit;
}

// Usuario tiene acceso - mostrar reproductor
?>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title><?= htmlspecialchars($event['title']) ?> - TenancingoLive</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 0; background: #000; color: #fff; }
        .header { background: rgba(0,0,0,0.8); padding: 15px; position: fixed; top: 0; left: 0; right: 0; z-index: 1000; }
        .user-info { float: right; }
        .video-container { margin-top: 60px; position: relative; width: 100%; height: calc(100vh - 60px); }
        video { width: 100%; height: 100%; object-fit: contain; }
        .chat { position: fixed; right: 0; top: 60px; width: 300px; height: calc(100vh - 60px); background: rgba(0,0,0,0.9); padding: 10px; overflow-y: auto; }
        .controls { position: absolute; bottom: 10px; left: 10px; background: rgba(0,0,0,0.7); padding: 10px; border-radius: 5px; }
        @media (max-width: 768px) { .chat { display: none; } }
    </style>
</head>
<body>
    <div class="header">
        <strong>🎪 <?= htmlspecialchars($event['title']) ?></strong>
        <div class="user-info">
            👤 <?= htmlspecialchars($userEmail) ?>
            <span id="viewer-count">• 0 espectadores</span>
        </div>
    </div>
    
    <div class="video-container">
        <video id="player" controls autoplay>
            <source src="<?= HLS_BASE_URL ?>/<?= htmlspecialchars($event['stream_key']) ?>.m3u8" type="application/x-mpegURL">
            Tu navegador no soporta streaming HLS
        </video>
        
        <div class="controls">
            <button onclick="toggleFullscreen()">🔳 Pantalla completa</button>
            <button onclick="toggleChat()">💬 Chat</button>
            <span id="stream-status">🔴 EN VIVO</span>
        </div>
    </div>
    
    <div class="chat" id="chat">
        <h4>💬 Chat en vivo</h4>
        <div id="chat-messages"></div>
        <input type="text" id="chat-input" placeholder="Escribe un mensaje..." style="width: 100%; margin-top: 10px;">
    </div>
    
    <script src="https://cdn.jsdelivr.net/npm/hls.js@latest"></script>
    <script>
        const video = document.getElementById('player');
        const videoSrc = '<?= HLS_BASE_URL ?>/<?= htmlspecialchars($event['stream_key']) ?>.m3u8';
        
        // Configurar HLS
        if (Hls.isSupported()) {
            const hls = new Hls();
            hls.loadSource(videoSrc);
            hls.attachMedia(video);
            
            hls.on(Hls.Events.MANIFEST_PARSED, function() {
                console.log('Stream cargado correctamente');
            });
            
            hls.on(Hls.Events.ERROR, function(event, data) {
                console.error('Error HLS:', data);
                document.getElementById('stream-status').textContent = '⚠️ Error de conexión';
            });
        } else if (video.canPlayType('application/vnd.apple.mpegurl')) {
            video.src = videoSrc;
        }
        
        // Funciones de control
        function toggleFullscreen() {
            if (document.fullscreenElement) {
                document.exitFullscreen();
            } else {
                video.requestFullscreen();
            }
        }
        
        function toggleChat() {
            const chat = document.getElementById('chat');
            chat.style.display = chat.style.display === 'none' ? 'block' : 'none';
        }
        
        // Actualizar contador de espectadores
        setInterval(() => {
            fetch('/api/viewer-count.php?event=<?= $eventId ?>')
                .then(r => r.json())
                .then(data => {
                    document.getElementById('viewer-count').textContent = `• ${data.count} espectadores`;
                });
        }, 30000);
        
        // Chat básico (WebSocket en producción)
        document.getElementById('chat-input').addEventListener('keypress', function(e) {
            if (e.key === 'Enter' && this.value.trim()) {
                // Enviar mensaje al chat
                console.log('Mensaje:', this.value);
                this.value = '';
            }
        });
    </script>
</body>
</html>