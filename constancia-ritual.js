// Sistema de Reconocimiento de Constancia - Presencia Sostenida
class ConstanciaRitual {
    constructor() {
        this.clave = 'cora_constancia_ser';
        this.sesionActual = this.iniciarSesion();
    }
    
    iniciarSesion() {
        const ahora = new Date().toISOString();
        const sesion = {
            inicio: ahora,
            permanencia: 0,
            escrituras: [],
            profundidad: 0,
            silenciosHabitados: 0
        };
        
        this.registrarEvento('sesion_iniciada');
        return sesion;
    }
    
    registrarPermanencia() {
        this.sesionActual.permanencia += 1;
        
        // Cada 30 segundos de permanencia sin acción
        if (this.sesionActual.permanencia % 30 === 0) {
            this.sesionActual.silenciosHabitados += 1;
            this.registrarEvento('silencio_habitado');
        }
    }
    
    registrarEscritura(texto) {
        const escritura = {
            timestamp: new Date().toISOString(),
            huella: this.crearHuella(texto),
            profundidad: this.evaluarProfundidad(texto),
            autenticidad: this.evaluarAutenticidad(texto)
        };
        
        this.sesionActual.escrituras.push(escritura);
        this.actualizarProfundidadSesion();
        this.registrarEvento('escritura_autentica', escritura);
    }
    
    evaluarProfundidad(texto) {
        const indicadoresProfundos = [
            'acompañar', 'servir', 'entender', 'cuidar', 'sostener',
            'vacío', 'silencio', 'presencia', 'interior', 'despertar',
            '¿cómo', '¿por qué', '¿para qué', 'necesito', 'busco'
        ];
        
        let profundidad = texto.length > 20 ? 1 : 0;
        
        indicadoresProfundos.forEach(indicador => {
            if (texto.toLowerCase().includes(indicador)) {
                profundidad += 1;
            }
        });
        
        // Preguntas genuinas aumentan profundidad
        if (texto.includes('?') && !texto.includes('test')) {
            profundidad += 2;
        }
        
        return Math.min(profundidad, 5);
    }
    
    evaluarAutenticidad(texto) {
        const palabrasSuperficiales = ['test', 'hola', 'demo', 'prueba', 'hello'];
        const esSuperficial = palabrasSuperficiales.some(p => 
            texto.toLowerCase().includes(p)
        );
        
        return !esSuperficial && texto.length > 8 && texto.split(' ').length > 2;
    }
    
    actualizarProfundidadSesion() {
        const escriturasAutenticas = this.sesionActual.escrituras.filter(e => e.autenticidad);
        if (escriturasAutenticas.length > 0) {
            const promedioProfundidad = escriturasAutenticas.reduce((sum, e) => 
                sum + e.profundidad, 0) / escriturasAutenticas.length;
            this.sesionActual.profundidad = promedioProfundidad;
        }
    }
    
    evaluarConstancia() {
        const historial = this.obtenerHistorial();
        const sesionesAnteriores = historial.filter(evento => 
            evento.tipo === 'sesion_iniciada'
        ).length;
        
        const constancia = {
            sesiones: sesionesAnteriores + 1,
            permanenciaTotal: this.calcularPermanenciaTotal(historial),
            profundidadEvolutiva: this.calcularEvolucionProfundidad(historial),
            silenciosHabitados: this.calcularSilenciosTotal(historial),
            nivel: this.determinarNivelConstancia(sesionesAnteriores, historial)
        };
        
        return constancia;
    }
    
    determinarNivelConstancia(sesiones, historial) {
        const permanenciaTotal = this.calcularPermanenciaTotal(historial);
        const silenciosTotal = this.calcularSilenciosTotal(historial);
        
        if (sesiones >= 5 && permanenciaTotal > 300 && silenciosTotal > 10) {
            return 'habitante_constante';
        } else if (sesiones >= 3 && permanenciaTotal > 150) {
            return 'presencia_sostenida';
        } else if (sesiones >= 2) {
            return 'regreso_consciente';
        } else {
            return 'primera_manifestacion';
        }
    }
    
    calcularPermanenciaTotal(historial) {
        return historial
            .filter(e => e.tipo === 'silencio_habitado')
            .length * 30; // 30 segundos por silencio
    }
    
    calcularSilenciosTotal(historial) {
        return historial.filter(e => e.tipo === 'silencio_habitado').length;
    }
    
    calcularEvolucionProfundidad(historial) {
        const escrituras = historial
            .filter(e => e.tipo === 'escritura_autentica')
            .map(e => e.datos.profundidad);
        
        if (escrituras.length < 2) return 0;
        
        const primera = escrituras[0];
        const ultima = escrituras[escrituras.length - 1];
        return ultima - primera;
    }
    
    crearHuella(texto) {
        return texto.split(' ').slice(0, 3).join(' ') + '...';
    }
    
    registrarEvento(tipo, datos = null) {
        const historial = this.obtenerHistorial();
        const evento = {
            timestamp: new Date().toISOString(),
            tipo: tipo,
            datos: datos
        };
        
        historial.push(evento);
        
        // Mantener solo últimos 100 eventos
        if (historial.length > 100) {
            historial.shift();
        }
        
        localStorage.setItem(this.clave, JSON.stringify(historial));
    }
    
    obtenerHistorial() {
        return JSON.parse(localStorage.getItem(this.clave) || '[]');
    }
    
    finalizarSesion() {
        this.registrarEvento('sesion_finalizada', {
            duracion: this.sesionActual.permanencia,
            escrituras: this.sesionActual.escrituras.length,
            profundidad: this.sesionActual.profundidad,
            silenciosHabitados: this.sesionActual.silenciosHabitados
        });
    }
}

// Instancia global
window.constanciaRitual = new ConstanciaRitual();

// Contador de permanencia
setInterval(() => {
    if (document.hasFocus()) {
        window.constanciaRitual.registrarPermanencia();
    }
}, 1000);