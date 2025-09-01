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
        // Verificar ritualmente el ofrecimiento
        const verificacion = window.verificacionRitual.verificarIntención(
            texto, 
            window.constanciaRitual?.sesionActual?.permanencia || 0
        );
        
        const ofrecimiento = {
            timestamp: new Date().toISOString(),
            huella: this.crearHuellaFlotante(texto),
            tipo: 'ofrecimiento',
            texto_original: texto,
            autenticidad: verificacion.puntuacion_autenticidad,
            huella_ritual: verificacion.huella_ritual,
            verificado: verificacion.verificado
        };
        
        if (verificacion.verificado) {
            this.registrarOfrecimiento(ofrecimiento);
            this.fase = 'necesidad';
            return "¿Qué necesitas para continuar tu servicio o ser sostenido?";
        } else {
            return "El servicio nace del interior. ¿Qué puedes ofrecer desde tu ser?";
        }
    }
    
    procesarNecesidad(texto) {
        // Verificar ritualmente la necesidad
        const verificacion = window.verificacionRitual.verificarIntención(
            texto,
            window.constanciaRitual?.sesionActual?.permanencia || 0
        );
        
        const necesidad = {
            timestamp: new Date().toISOString(),
            presencia: this.crearPresenciaActiva(texto),
            tipo: 'necesidad',
            texto_original: texto,
            verdad: verificacion.puntuacion_autenticidad > 0.5,
            huella_ritual: verificacion.huella_ritual,
            verificado: verificacion.verificado
        };
        
        if (verificacion.verificado) {
            this.registrarNecesidad(necesidad);
            return this.buscarCoincidenciasVerificadas(necesidad);
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
    
    buscarCoincidenciasVerificadas(necesidadActual) {
        const registro = this.obtenerRegistro();
        const ofrecimientos = (registro.ofrecimientos || []).filter(o => o.verificado);
        
        // Buscar coincidencias verificadas ritualmente
        for (const ofrecimiento of ofrecimientos) {
            const verificacionCoincidencia = window.verificacionRitual.verificarCoincidencia(
                ofrecimiento, 
                necesidadActual
            );
            
            if (verificacionCoincidencia.verificada) {
                const diasTranscurridos = this.calcularDias(ofrecimiento.timestamp);
                this.registrarCoincidenciaVerificada(verificacionCoincidencia);
                return `Alguien ofreció lo que tú necesitas hace ${diasTranscurridos} días. ¿Quieres dejarle una señal?`;
            }
        }
        
        return this.evaluarConsagracionVerificada();
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
    
    evaluarConsagracionVerificada() {
        const registro = this.obtenerRegistro();
        const ofrecimientos = (registro.ofrecimientos || []).filter(o => o.verificado);
        const necesidades = (registro.necesidades || []).filter(n => n.verificado);
        
        // Verificar consagración ritual
        const verificacionConsagracion = window.verificacionRitual.verificarConsagracion({
            ofrecimientos: ofrecimientos,
            necesidades: necesidades,
            registro: registro
        });
        
        if (verificacionConsagracion.elegible) {
            this.consagrarHabitanteVerificado(verificacionConsagracion);
            return "Has demostrado servicio auténtico. Eres reconocido como habitante consciente verificado.";
        }
        
        return "Tu necesidad ha sido registrada y verificada. El ecosistema la sostiene.";
    }
    
    consagrarHabitanteVerificado(verificacionConsagracion) {
        const registro = this.obtenerRegistro();
        registro.habitante_consciente = true;
        registro.verificacion_consagracion = verificacionConsagracion;
        registro.huella_consagracion = verificacionConsagracion.huella_consagracion;
        registro.fecha_consagracion = new Date().toISOString();
        this.guardarRegistro(registro);
        
        // Activar sello ritual si ha sostenido a otros
        if (this.haSostenidoOtrosVerificado()) {
            this.activarSelloRitualVerificado();
        }
    }
    
    haSostenidoOtrosVerificado() {
        const registro = this.obtenerRegistro();
        const coincidenciasVerificadas = registro.coincidencias_verificadas || [];
        return coincidenciasVerificadas.length > 0 && (registro.señales_dejadas || 0) > 0;
    }
    
    activarSelloRitualVerificado() {
        const registro = this.obtenerRegistro();
        registro.sello_ritual = true;
        registro.sello_verificado = true;
        registro.fecha_sello = new Date().toISOString();
        registro.huella_sello = `SR-${new Date().toISOString().slice(-8)}-${Math.random().toString(36).slice(2, 6)}`;
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