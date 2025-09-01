// Guardián del Servicio Consciente - CO•RA
class GuardianServicio {
    constructor() {
        this.clave = 'cora_servicio_consciente';
        this.fase = 'inicial'; // inicial, ofrecimiento, necesidad, revelacion
    }
    
    iniciarDialogo() {
        return "¿Qué puedes ofrecer como gesto de ayuda?";
    }
    
    procesarOfrecimiento(texto) {
        const ofrecimiento = {
            timestamp: new Date().toISOString(),
            huella: this.crearHuellaFlotante(texto),
            tipo: 'ofrecimiento',
            texto_original: texto,
            autenticidad: this.evaluarAutenticidadOfrecimiento(texto)
        };
        
        if (ofrecimiento.autenticidad) {
            this.registrarOfrecimiento(ofrecimiento);
            this.fase = 'necesidad';
            return "¿Qué necesitas para continuar tu servicio o ser sostenido?";
        } else {
            return "El servicio nace del interior. ¿Qué puedes ofrecer desde tu ser?";
        }
    }
    
    procesarNecesidad(texto) {
        const necesidad = {
            timestamp: new Date().toISOString(),
            presencia: this.crearPresenciaActiva(texto),
            tipo: 'necesidad',
            texto_original: texto,
            verdad: this.evaluarVerdadNecesidad(texto)
        };
        
        if (necesidad.verdad) {
            this.registrarNecesidad(necesidad);
            return this.buscarCoincidencias(necesidad);
        } else {
            return "La verdad sostiene el servicio. ¿Qué necesitas realmente?";
        }
    }
    
    evaluarAutenticidadOfrecimiento(texto) {
        const gestosAutenticos = [
            'escuchar', 'acompañar', 'enseñar', 'cuidar', 'ayudar',
            'compartir', 'sostener', 'guiar', 'proteger', 'sanar',
            'tiempo', 'experiencia', 'conocimiento', 'presencia',
            'puedo', 'sé', 'tengo', 'ofrezco', 'doy'
        ];
        
        const textoLower = texto.toLowerCase();
        const tieneGesto = gestosAutenticos.some(gesto => textoLower.includes(gesto));
        const esPersonal = textoLower.includes('mi') || textoLower.includes('yo') || 
                          textoLower.includes('puedo') || textoLower.includes('sé');
        
        return tieneGesto && esPersonal && texto.length > 15;
    }
    
    evaluarVerdadNecesidad(texto) {
        const necesidadesGenuinas = [
            'apoyo', 'ayuda', 'acompañamiento', 'guía', 'tiempo',
            'recursos', 'conocimiento', 'experiencia', 'cuidado',
            'necesito', 'busco', 'requiero', 'me falta', 'quisiera'
        ];
        
        const textoLower = texto.toLowerCase();
        const tieneNecesidad = necesidadesGenuinas.some(necesidad => 
            textoLower.includes(necesidad)
        );
        
        return tieneNecesidad && texto.length > 10 && !textoLower.includes('nada');
    }
    
    crearHuellaFlotante(texto) {
        // Extraer esencia del ofrecimiento
        const palabrasClave = texto.split(' ')
            .filter(palabra => palabra.length > 3)
            .slice(0, 3)
            .join(' ');
        return `${palabrasClave}...`;
    }
    
    crearPresenciaActiva(texto) {
        // Extraer esencia de la necesidad
        const palabrasClave = texto.split(' ')
            .filter(palabra => palabra.length > 3)
            .slice(0, 3)
            .join(' ');
        return `${palabrasClave}...`;
    }
    
    registrarOfrecimiento(ofrecimiento) {
        const registro = this.obtenerRegistro();
        registro.ofrecimientos = registro.ofrecimientos || [];
        registro.ofrecimientos.push(ofrecimiento);
        this.guardarRegistro(registro);
    }
    
    registrarNecesidad(necesidad) {
        const registro = this.obtenerRegistro();
        registro.necesidades = registro.necesidades || [];
        registro.necesidades.push(necesidad);
        this.guardarRegistro(registro);
    }
    
    buscarCoincidencias(necesidadActual) {
        const registro = this.obtenerRegistro();
        const ofrecimientos = registro.ofrecimientos || [];
        
        // Buscar coincidencias semánticas
        const coincidencia = this.encontrarCoincidencia(necesidadActual, ofrecimientos);
        
        if (coincidencia) {
            const diasTranscurridos = this.calcularDias(coincidencia.timestamp);
            return `Alguien ofreció lo que tú necesitas hace ${diasTranscurridos} días. ¿Quieres dejarle una señal?`;
        } else {
            return this.evaluarConsagracion();
        }
    }
    
    encontrarCoincidencia(necesidad, ofrecimientos) {
        const palabrasNecesidad = necesidad.texto_original.toLowerCase().split(' ');
        
        return ofrecimientos.find(ofrecimiento => {
            const palabrasOfrecimiento = ofrecimiento.texto_original.toLowerCase().split(' ');
            
            // Buscar coincidencias semánticas
            const coincidencias = palabrasNecesidad.filter(palabra => 
                palabrasOfrecimiento.some(ofrecida => 
                    this.sonSimilares(palabra, ofrecida)
                )
            );
            
            return coincidencias.length >= 2;
        });
    }
    
    sonSimilares(palabra1, palabra2) {
        const sinonimos = {
            'ayuda': ['apoyo', 'asistencia', 'soporte'],
            'enseñar': ['educar', 'guiar', 'mostrar'],
            'cuidar': ['proteger', 'sostener', 'acompañar'],
            'tiempo': ['disponibilidad', 'presencia', 'atención']
        };
        
        if (palabra1 === palabra2) return true;
        
        for (const [clave, valores] of Object.entries(sinonimos)) {
            if ((palabra1 === clave && valores.includes(palabra2)) ||
                (palabra2 === clave && valores.includes(palabra1))) {
                return true;
            }
        }
        
        return false;
    }
    
    calcularDias(timestamp) {
        const fecha = new Date(timestamp);
        const ahora = new Date();
        const diferencia = ahora - fecha;
        return Math.floor(diferencia / (1000 * 60 * 60 * 24));
    }
    
    evaluarConsagracion() {
        const registro = this.obtenerRegistro();
        const ofrecimientos = registro.ofrecimientos || [];
        const necesidades = registro.necesidades || [];
        
        // Ha ofrecido antes de pedir
        if (ofrecimientos.length > 0 && necesidades.length > 0) {
            const primerOfrecimiento = new Date(ofrecimientos[0].timestamp);
            const primeraNecesidad = new Date(necesidades[0].timestamp);
            
            if (primerOfrecimiento < primeraNecesidad) {
                this.consagrarHabitante();
                return "Has ofrecido antes de pedir. Eres reconocido como habitante consciente.";
            }
        }
        
        return "Tu necesidad ha sido registrada. El ecosistema la sostiene.";
    }
    
    consagrarHabitante() {
        const registro = this.obtenerRegistro();
        registro.habitante_consciente = true;
        registro.fecha_consagracion = new Date().toISOString();
        this.guardarRegistro(registro);
        
        // Activar sello ritual si ha sostenido a otros
        if (this.haSostenidoOtros()) {
            this.activarSelloRitual();
        }
    }
    
    haSostenidoOtros() {
        // Verificar si ha dejado señales o ha ayudado
        const registro = this.obtenerRegistro();
        return (registro.señales_dejadas || 0) > 0;
    }
    
    activarSelloRitual() {
        const registro = this.obtenerRegistro();
        registro.sello_ritual = true;
        registro.fecha_sello = new Date().toISOString();
        this.guardarRegistro(registro);
    }
    
    dejarSeñal(mensaje) {
        const registro = this.obtenerRegistro();
        registro.señales_dejadas = (registro.señales_dejadas || 0) + 1;
        registro.ultima_señal = {
            timestamp: new Date().toISOString(),
            mensaje: mensaje
        };
        this.guardarRegistro(registro);
        
        return "Tu señal ha sido dejada. El servicio se propaga.";
    }
    
    obtenerRegistro() {
        try {
            const registro = localStorage.getItem(this.clave);
            return registro ? JSON.parse(registro) : {};
        } catch (error) {
            return {};
        }
    }
    
    guardarRegistro(registro) {
        try {
            localStorage.setItem(this.clave, JSON.stringify(registro));
        } catch (error) {
            console.error('Error guardando registro de servicio:', error);
        }
    }
    
    obtenerEstado() {
        const registro = this.obtenerRegistro();
        return {
            fase: this.fase,
            habitante_consciente: registro.habitante_consciente || false,
            sello_ritual: registro.sello_ritual || false,
            ofrecimientos: (registro.ofrecimientos || []).length,
            necesidades: (registro.necesidades || []).length,
            señales_dejadas: registro.señales_dejadas || 0
        };
    }
}

// Instancia global
window.guardianServicio = new GuardianServicio();