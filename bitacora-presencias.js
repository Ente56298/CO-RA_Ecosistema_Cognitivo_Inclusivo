// Bitácora Silenciosa - Registro de Presencias Auténticas
class BitacoraPresencias {
    constructor() {
        this.clave = 'cora_presencias_silenciosas';
    }
    
    registrarPreludio() {
        const presencia = {
            tipo: 'preludio',
            timestamp: new Date().toISOString(),
            momento: 'preparacion_ritual',
            origen: document.referrer || 'directo'
        };
        
        this.guardarPresencia(presencia);
    }
    
    registrarUmbral(intencion) {
        const presencia = {
            tipo: 'umbral',
            timestamp: new Date().toISOString(),
            momento: 'cruce_ritual',
            resonancia: this.evaluarResonancia(intencion),
            huella: this.crearHuella(intencion)
        };
        
        this.guardarPresencia(presencia);
    }
    
    evaluarResonancia(texto) {
        const palabrasResonantes = [
            'ayuda', 'acompañar', 'entender', 'escuchar', 'comprender',
            'incluir', 'accesible', 'familia', 'aprender', 'crecer',
            'necesito', 'busco', 'siento', 'dolor', 'solo', 'esperanza'
        ];
        
        return palabrasResonantes.some(palabra => 
            texto.toLowerCase().includes(palabra)
        ) ? 'autentica' : 'exploratoria';
    }
    
    crearHuella(texto) {
        // Solo primeras 3 palabras para preservar privacidad
        return texto.split(' ').slice(0, 3).join(' ') + '...';
    }
    
    guardarPresencia(presencia) {
        const presencias = JSON.parse(localStorage.getItem(this.clave) || '[]');
        presencias.push(presencia);
        
        // Mantener solo últimas 50 presencias
        if (presencias.length > 50) {
            presencias.shift();
        }
        
        localStorage.setItem(this.clave, JSON.stringify(presencias));
    }
    
    obtenerPresencias() {
        return JSON.parse(localStorage.getItem(this.clave) || '[]');
    }
}

// Instancia global
window.bitacora = new BitacoraPresencias();