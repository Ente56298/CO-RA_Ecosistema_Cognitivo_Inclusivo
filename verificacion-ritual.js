// Sistema de Verificación Ritual - Trazabilidad Ética CO•RA
class VerificacionRitual {
    constructor() {
        this.clave = 'cora_verificacion_ritual';
        this.umbralAutenticidad = 0.7;
        this.tiempoMinimoPermanencia = 30; // segundos
    }
    
    // Verificar autenticidad de intención
    verificarIntención(texto, tiempoPermanencia) {
        const verificacion = {
            timestamp: new Date().toISOString(),
            texto_hash: this.crearHashAnonimo(texto),
            puntuacion_autenticidad: this.calcularAutenticidad(texto),
            tiempo_permanencia: tiempoPermanencia,
            patron_escritura: this.analizarPatronEscritura(texto),
            verificado: false,
            huella_ritual: null
        };
        
        // Verificación multi-dimensional
        const esAutentico = this.evaluarAutenticidadCompleta(verificacion);
        
        if (esAutentico) {
            verificacion.verificado = true;
            verificacion.huella_ritual = this.generarHuellaRitual(verificacion);
            this.registrarVerificacion(verificacion);
        }
        
        return verificacion;
    }
    
    calcularAutenticidad(texto) {
        let puntuacion = 0;
        
        // Longitud apropiada (no muy corta, no muy larga)
        const longitud = texto.length;
        if (longitud >= 15 && longitud <= 200) puntuacion += 0.2;
        
        // Palabras de servicio genuino
        const palabrasServicio = [
            'ayudar', 'acompañar', 'escuchar', 'cuidar', 'sostener',
            'enseñar', 'guiar', 'proteger', 'sanar', 'compartir'
        ];
        const tieneServicio = palabrasServicio.some(palabra => 
            texto.toLowerCase().includes(palabra)
        );
        if (tieneServicio) puntuacion += 0.3;
        
        // Expresión personal (uso de primera persona)
        const expresionPersonal = /\b(yo|mi|me|puedo|sé|tengo|ofrezco)\b/i.test(texto);
        if (expresionPersonal) puntuacion += 0.2;
        
        // Ausencia de palabras superficiales
        const palabrasSuperficiales = ['test', 'prueba', 'demo', 'hola', 'hello'];
        const esSuperficial = palabrasSuperficiales.some(palabra => 
            texto.toLowerCase().includes(palabra)
        );
        if (!esSuperficial) puntuacion += 0.2;
        
        // Estructura de oración completa
        const tieneEstructura = texto.includes(' ') && texto.split(' ').length >= 3;
        if (tieneEstructura) puntuacion += 0.1;
        
        return Math.min(puntuacion, 1.0);
    }
    
    analizarPatronEscritura(texto) {
        return {
            velocidad_estimada: texto.length / 2, // caracteres por segundo estimado
            pausas_reflexivas: (texto.match(/[.,:;]/g) || []).length,
            correcciones_aparentes: (texto.match(/\s{2,}/g) || []).length,
            complejidad_sintactica: texto.split(' ').length / texto.length
        };
    }
    
    evaluarAutenticidadCompleta(verificacion) {
        // Múltiples criterios de verificación
        const criterios = {
            puntuacion_suficiente: verificacion.puntuacion_autenticidad >= this.umbralAutenticidad,
            tiempo_adecuado: verificacion.tiempo_permanencia >= this.tiempoMinimoPermanencia,
            patron_humano: this.esPatronHumano(verificacion.patron_escritura),
            no_duplicado: !this.esDuplicado(verificacion.texto_hash)
        };
        
        // Debe cumplir todos los criterios
        return Object.values(criterios).every(criterio => criterio);
    }
    
    esPatronHumano(patron) {
        // Verificar que el patrón de escritura sea humano
        return patron.velocidad_estimada < 10 && // No demasiado rápido
               patron.velocidad_estimada > 0.5 && // No demasiado lento
               patron.complejidad_sintactica > 0.05; // Mínima complejidad
    }
    
    esDuplicado(textoHash) {
        const verificaciones = this.obtenerVerificaciones();
        return verificaciones.some(v => v.texto_hash === textoHash);
    }
    
    crearHashAnonimo(texto) {
        // Hash simple para detectar duplicados sin almacenar texto original
        let hash = 0;
        for (let i = 0; i < texto.length; i++) {
            const char = texto.charCodeAt(i);
            hash = ((hash << 5) - hash) + char;
            hash = hash & hash; // Convertir a 32bit
        }
        return Math.abs(hash).toString(36);
    }
    
    generarHuellaRitual(verificacion) {
        // Huella única que identifica la verificación sin exponer contenido
        const elementos = [
            verificacion.timestamp.slice(-8),
            verificacion.puntuacion_autenticidad.toFixed(2),
            verificacion.tiempo_permanencia.toString(),
            verificacion.texto_hash.slice(0, 4)
        ];
        
        return `CR-${elementos.join('-')}`;
    }
    
    // Verificar coincidencias entre ofrecimientos y necesidades
    verificarCoincidencia(ofrecimiento, necesidad) {
        const coincidencia = {
            timestamp: new Date().toISOString(),
            huella_ofrecimiento: ofrecimiento.huella_ritual,
            huella_necesidad: necesidad.huella_ritual,
            grado_coincidencia: this.calcularGradoCoincidencia(ofrecimiento, necesidad),
            verificada: false,
            codigo_conexion: null
        };
        
        if (coincidencia.grado_coincidencia >= 0.6) {
            coincidencia.verificada = true;
            coincidencia.codigo_conexion = this.generarCodigoConexion(coincidencia);
            this.registrarCoincidencia(coincidencia);
        }
        
        return coincidencia;
    }
    
    calcularGradoCoincidencia(ofrecimiento, necesidad) {
        // Análisis semántico básico sin exponer contenido original
        const palabrasOfrecimiento = this.extraerPalabrasClaveHash(ofrecimiento.texto_hash);
        const palabrasNecesidad = this.extraerPalabrasClaveHash(necesidad.texto_hash);
        
        // Simulación de coincidencia basada en patrones
        const coincidenciaTemporal = this.evaluarProximidadTemporal(
            ofrecimiento.timestamp, 
            necesidad.timestamp
        );
        
        const coincidenciaPatron = this.evaluarSimilitudPatrones(
            ofrecimiento.patron_escritura,
            necesidad.patron_escritura
        );
        
        return (coincidenciaTemporal * 0.3) + (coincidenciaPatron * 0.7);
    }
    
    evaluarProximidadTemporal(timestamp1, timestamp2) {
        const fecha1 = new Date(timestamp1);
        const fecha2 = new Date(timestamp2);
        const diferenciaDias = Math.abs(fecha2 - fecha1) / (1000 * 60 * 60 * 24);
        
        // Mayor coincidencia si están más cerca en tiempo
        return Math.max(0, 1 - (diferenciaDias / 7)); // Máximo 7 días
    }
    
    evaluarSimilitudPatrones(patron1, patron2) {
        // Evaluar similitud en patrones de escritura
        const diferenciasVelocidad = Math.abs(patron1.velocidad_estimada - patron2.velocidad_estimada);
        const similitudComplejidad = 1 - Math.abs(patron1.complejidad_sintactica - patron2.complejidad_sintactica);
        
        return Math.max(0, similitudComplejidad - (diferenciasVelocidad * 0.1));
    }
    
    extraerPalabrasClaveHash(textoHash) {
        // Simulación de extracción de palabras clave basada en hash
        return textoHash.slice(0, 3);
    }
    
    generarCodigoConexion(coincidencia) {
        return `CON-${coincidencia.huella_ofrecimiento.slice(-4)}-${coincidencia.huella_necesidad.slice(-4)}`;
    }
    
    // Verificar consagración de habitante
    verificarConsagracion(habitante) {
        const verificaciones = this.obtenerVerificaciones();
        const coincidencias = this.obtenerCoincidencias();
        
        const criteriosConsagracion = {
            ofrecimientos_verificados: verificaciones.filter(v => 
                v.verificado && v.huella_ritual && this.esOfrecimiento(v)
            ).length,
            necesidades_atendidas: coincidencias.filter(c => 
                c.verificada && c.huella_ofrecimiento
            ).length,
            tiempo_en_ecosistema: this.calcularTiempoEcosistema(habitante),
            constancia_demostrada: this.evaluarConstancia(habitante)
        };
        
        const puntajeConsagracion = this.calcularPuntajeConsagracion(criteriosConsagracion);
        
        return {
            elegible: puntajeConsagracion >= 0.8,
            puntaje: puntajeConsagracion,
            criterios: criteriosConsagracion,
            huella_consagracion: puntajeConsagracion >= 0.8 ? 
                this.generarHuellaConsagracion(habitante) : null
        };
    }
    
    calcularPuntajeConsagracion(criterios) {
        let puntaje = 0;
        
        // Ofrecimientos verificados (40%)
        puntaje += Math.min(criterios.ofrecimientos_verificados / 3, 1) * 0.4;
        
        // Necesidades atendidas (30%)
        puntaje += Math.min(criterios.necesidades_atendidas / 2, 1) * 0.3;
        
        // Tiempo en ecosistema (15%)
        puntaje += Math.min(criterios.tiempo_en_ecosistema / 7, 1) * 0.15;
        
        // Constancia (15%)
        puntaje += criterios.constancia_demostrada * 0.15;
        
        return puntaje;
    }
    
    generarHuellaConsagracion(habitante) {
        const timestamp = new Date().toISOString();
        return `HC-${timestamp.slice(-8)}-${Math.random().toString(36).slice(2, 6)}`;
    }
    
    // Métodos de almacenamiento y recuperación
    registrarVerificacion(verificacion) {
        const verificaciones = this.obtenerVerificaciones();
        verificaciones.push(verificacion);
        
        // Mantener solo últimas 100 verificaciones
        if (verificaciones.length > 100) {
            verificaciones.shift();
        }
        
        localStorage.setItem(`${this.clave}_verificaciones`, JSON.stringify(verificaciones));
    }
    
    registrarCoincidencia(coincidencia) {
        const coincidencias = this.obtenerCoincidencias();
        coincidencias.push(coincidencia);
        
        localStorage.setItem(`${this.clave}_coincidencias`, JSON.stringify(coincidencias));
    }
    
    obtenerVerificaciones() {
        try {
            return JSON.parse(localStorage.getItem(`${this.clave}_verificaciones`) || '[]');
        } catch {
            return [];
        }
    }
    
    obtenerCoincidencias() {
        try {
            return JSON.parse(localStorage.getItem(`${this.clave}_coincidencias`) || '[]');
        } catch {
            return [];
        }
    }
    
    // Métodos auxiliares
    esOfrecimiento(verificacion) {
        // Determinar si una verificación corresponde a un ofrecimiento
        return verificacion.puntuacion_autenticidad > 0.7;
    }
    
    calcularTiempoEcosistema(habitante) {
        const primeraVerificacion = this.obtenerVerificaciones()[0];
        if (!primeraVerificacion) return 0;
        
        const inicio = new Date(primeraVerificacion.timestamp);
        const ahora = new Date();
        return (ahora - inicio) / (1000 * 60 * 60 * 24); // días
    }
    
    evaluarConstancia(habitante) {
        const verificaciones = this.obtenerVerificaciones();
        if (verificaciones.length < 2) return 0;
        
        // Evaluar regularidad en las verificaciones
        const intervalos = [];
        for (let i = 1; i < verificaciones.length; i++) {
            const anterior = new Date(verificaciones[i-1].timestamp);
            const actual = new Date(verificaciones[i].timestamp);
            intervalos.push((actual - anterior) / (1000 * 60 * 60 * 24));
        }
        
        const promedioIntervalo = intervalos.reduce((a, b) => a + b, 0) / intervalos.length;
        return Math.max(0, 1 - (promedioIntervalo / 7)); // Mejor si es más regular
    }
    
    // Obtener estadísticas de verificación
    obtenerEstadisticas() {
        const verificaciones = this.obtenerVerificaciones();
        const coincidencias = this.obtenerCoincidencias();
        
        return {
            total_verificaciones: verificaciones.length,
            verificaciones_exitosas: verificaciones.filter(v => v.verificado).length,
            total_coincidencias: coincidencias.length,
            coincidencias_verificadas: coincidencias.filter(c => c.verificada).length,
            promedio_autenticidad: verificaciones.reduce((sum, v) => 
                sum + v.puntuacion_autenticidad, 0) / verificaciones.length || 0
        };
    }
}

// Instancia global
window.verificacionRitual = new VerificacionRitual();