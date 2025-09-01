// Sistema de Escenarios Rituales - CO•RA
class EscenariosRituales {
    constructor() {
        this.clave = 'cora_escenarios_rituales';
        this.escenariosActivos = new Map();
        this.donacionesConscientes = new Map();
    }
    
    // Activar donaciones conscientes
    activarDonacionesConscientes() {
        const moduloDonaciones = {
            verificarNecesidadReal: (necesidad, habitante) => {
                const criterios = {
                    intencion_autentica: this.verificarIntencionAutentica(necesidad),
                    ha_ofrecido_antes: habitante.ofrecimientos_verificados > 0,
                    vibra_con_verdad: this.evaluarVerdadNecesidad(necesidad),
                    sostenido_por_otro: habitante.señales_dejadas > 0
                };
                
                const puntaje = Object.values(criterios).filter(Boolean).length;
                return {
                    verificada: puntaje >= 3,
                    criterios: criterios,
                    huella_necesidad: this.generarHuellaNecesidad(necesidad)
                };
            },
            
            registrarNecesidadReal: (necesidad, verificacion) => {
                if (verificacion.verificada) {
                    const registro = {
                        timestamp: new Date().toISOString(),
                        huella: verificacion.huella_necesidad,
                        tipo: 'necesidad_real',
                        estado: 'activa',
                        criterios_cumplidos: verificacion.criterios
                    };
                    
                    this.donacionesConscientes.set(registro.huella, registro);
                    this.persistirDonaciones();
                    return registro;
                }
                return null;
            },
            
            buscarCoincidenciasApoyo: (necesidad) => {
                const oferentes = window.nichosServicio.habitantesOferentes;
                const coincidencias = [];
                
                for (const [id, oferente] of oferentes) {
                    if (oferente.disponibilidad === 'activa') {
                        const compatibilidad = this.evaluarCompatibilidadApoyo(necesidad, oferente);
                        if (compatibilidad > 0.7) {
                            coincidencias.push({
                                oferente_huella: oferente.huella_servicio,
                                compatibilidad: compatibilidad,
                                tipo_apoyo: this.determinarTipoApoyo(oferente.habilidades)
                            });
                        }
                    }
                }
                
                return coincidencias.sort((a, b) => b.compatibilidad - a.compatibilidad);
            }
        };
        
        return moduloDonaciones;
    }
    
    // Crear oficina simbólica física
    crearOficinaFisica(ubicacion, responsable, tipoEspacio) {
        const oficina = {
            id: this.generarIdOficina(),
            ubicacion: ubicacion,
            tipo_espacio: tipoEspacio, // biblioteca, centro_comunitario, escuela
            responsable_huella: responsable.huella_consagracion,
            timestamp_creacion: new Date().toISOString(),
            activadores_disponibles: this.generarActivadores(),
            distribuciones_realizadas: 0,
            estado: 'activa'
        };
        
        this.registrarOficinaFisica(oficina);
        return oficina;
    }
    
    generarActivadores() {
        return {
            qr_codes: [
                `${window.location.origin}/activacion-qr.html?oficina=${Date.now()}`,
                `${window.location.origin}/index.html?origen=oficina_simbolica`
            ],
            frases_flotantes: [
                "CO•RA no se abre. Se revela.",
                "Quien vive para servir, sirve para vivir.",
                "¿Qué puedes ofrecer como gesto de ayuda?"
            ],
            tarjetas_rituales: this.generarTarjetasRituales()
        };
    }
    
    generarTarjetasRituales() {
        return [
            {
                texto: "Escribe con intención.",
                url: `${window.location.origin}/index.html`,
                codigo: `TR-${Date.now().toString(36).slice(-4)}`
            },
            {
                texto: "El núcleo no se abre. Se revela.",
                url: `${window.location.origin}/index.html`,
                codigo: `TR-${Date.now().toString(36).slice(-4)}`
            }
        ];
    }
    
    // Activar escenario comunitario
    activarEscenarioComunitario(tipoEscenario, ubicacion, parametros) {
        const escenarios = {
            'feria_servicio_etico': () => this.crearFeriaServicio(ubicacion, parametros),
            'jornada_activacion': () => this.crearJornadaActivacion(ubicacion, parametros),
            'taller_reconocimiento': () => this.crearTallerReconocimiento(ubicacion, parametros),
            'mesa_acompañamiento': () => this.crearMesaAcompañamiento(ubicacion, parametros),
            'distribucion_recursos': () => this.crearDistribucionRecursos(ubicacion, parametros)
        };
        
        const escenario = escenarios[tipoEscenario]?.();
        if (escenario) {
            this.escenariosActivos.set(escenario.id, escenario);
            this.persistirEscenarios();
        }
        
        return escenario;
    }
    
    crearFeriaServicio(ubicacion, parametros) {
        return {
            id: `FS-${Date.now().toString(36)}`,
            tipo: 'feria_servicio_etico',
            ubicacion: ubicacion,
            fecha_inicio: parametros.fecha_inicio,
            duracion_horas: parametros.duracion || 8,
            oferentes_esperados: parametros.oferentes || 10,
            activadores_generados: this.generarActivadores(),
            estado: 'programada'
        };
    }
    
    crearMesaAcompañamiento(ubicacion, parametros) {
        return {
            id: `MA-${Date.now().toString(36)}`,
            tipo: 'mesa_acompañamiento',
            ubicacion: ubicacion,
            servicios_disponibles: ['escucha', 'orientacion', 'diseño_etico'],
            horarios: parametros.horarios || '9:00-17:00',
            responsable: parametros.responsable,
            activaciones_diarias: 0,
            estado: 'activa'
        };
    }
    
    crearDistribucionRecursos(ubicacion, parametros) {
        return {
            id: `DR-${Date.now().toString(36)}`,
            tipo: 'distribucion_recursos',
            ubicacion: ubicacion,
            recursos_disponibles: parametros.recursos || [],
            criterios_distribucion: 'verificacion_ritual',
            entregas_realizadas: 0,
            red_externa: parametros.red_externa, // INAES, Fonart, etc.
            estado: 'activa'
        };
    }
    
    // Verificar necesidad real para donaciones
    verificarIntencionAutentica(necesidad) {
        const indicadores = [
            'continuar mi servicio', 'seguir ayudando', 'sostener mi trabajo',
            'necesito apoyo para', 'situación difícil pero', 'quiero seguir'
        ];
        
        return indicadores.some(indicador => 
            necesidad.toLowerCase().includes(indicador)
        );
    }
    
    evaluarVerdadNecesidad(necesidad) {
        const palabrasVerdad = [
            'realmente', 'genuinamente', 'honestamente', 'verdaderamente',
            'necesito', 'requiero', 'me hace falta', 'es esencial'
        ];
        
        const palabrasUtilidad = [
            'quiero', 'deseo', 'me gustaría', 'sería bueno', 'prefiero'
        ];
        
        const tieneVerdad = palabrasVerdad.some(p => necesidad.toLowerCase().includes(p));
        const soloUtilidad = palabrasUtilidad.some(p => necesidad.toLowerCase().includes(p));
        
        return tieneVerdad && !soloUtilidad;
    }
    
    evaluarCompatibilidadApoyo(necesidad, oferente) {
        // Evaluar si el oferente puede ayudar con la necesidad
        const necesidadProcesada = necesidad.toLowerCase();
        let compatibilidad = 0;
        
        oferente.habilidades.forEach(habilidad => {
            const habilidadLower = habilidad.descripcion.toLowerCase();
            
            // Coincidencias directas
            if (necesidadProcesada.includes('económico') && habilidadLower.includes('apoyo')) {
                compatibilidad += 0.4;
            }
            if (necesidadProcesada.includes('emocional') && habilidadLower.includes('acompañar')) {
                compatibilidad += 0.4;
            }
            if (necesidadProcesada.includes('técnico') && habilidadLower.includes('diseñar')) {
                compatibilidad += 0.4;
            }
        });
        
        return Math.min(compatibilidad, 1.0);
    }
    
    determinarTipoApoyo(habilidades) {
        const tipos = {
            'economico': ['apoyo', 'recursos', 'financiero'],
            'emocional': ['acompañar', 'escuchar', 'sostener'],
            'tecnico': ['diseñar', 'programar', 'crear'],
            'educativo': ['enseñar', 'guiar', 'explicar']
        };
        
        for (const [tipo, palabras] of Object.entries(tipos)) {
            const tieneHabilidad = habilidades.some(h => 
                palabras.some(p => h.descripcion.toLowerCase().includes(p))
            );
            if (tieneHabilidad) return tipo;
        }
        
        return 'general';
    }
    
    generarHuellaNecesidad(necesidad) {
        const palabrasClave = necesidad.split(' ')
            .filter(p => p.length > 3)
            .slice(0, 3)
            .join('-');
        return `HN-${palabrasClave}-${Date.now().toString(36).slice(-4)}`;
    }
    
    generarIdOficina() {
        return `OF-${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 4)}`;
    }
    
    // Métodos de persistencia
    persistirEscenarios() {
        const escenarios = Array.from(this.escenariosActivos.entries());
        localStorage.setItem(`${this.clave}_escenarios`, JSON.stringify(escenarios));
    }
    
    persistirDonaciones() {
        const donaciones = Array.from(this.donacionesConscientes.entries());
        localStorage.setItem(`${this.clave}_donaciones`, JSON.stringify(donaciones));
    }
    
    registrarOficinaFisica(oficina) {
        const oficinas = this.obtenerOficinasActivas();
        oficinas.push(oficina);
        localStorage.setItem(`${this.clave}_oficinas_fisicas`, JSON.stringify(oficinas));
    }
    
    obtenerOficinasActivas() {
        try {
            return JSON.parse(localStorage.getItem(`${this.clave}_oficinas_fisicas`) || '[]');
        } catch {
            return [];
        }
    }
    
    obtenerEscenarios() {
        try {
            const escenarios = JSON.parse(localStorage.getItem(`${this.clave}_escenarios`) || '[]');
            return new Map(escenarios);
        } catch {
            return new Map();
        }
    }
    
    // Obtener estadísticas de impacto
    obtenerEstadisticasImpacto() {
        return {
            escenarios_activos: this.escenariosActivos.size,
            oficinas_fisicas: this.obtenerOficinasActivas().length,
            donaciones_verificadas: this.donacionesConscientes.size,
            activaciones_totales: this.calcularActivacionesTotales(),
            ultima_actualizacion: new Date().toISOString()
        };
    }
    
    calcularActivacionesTotales() {
        const oficinas = this.obtenerOficinasActivas();
        return oficinas.reduce((total, oficina) => 
            total + (oficina.activaciones_realizadas || 0), 0
        );
    }
}

// Instancia global
window.escenariosRituales = new EscenariosRituales();