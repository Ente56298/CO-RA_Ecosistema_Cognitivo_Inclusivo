// Protocolo de Contingencias CO•RA - Respuesta Ética en Crisis
class ProtocoloContingencias {
    constructor() {
        this.clave = 'cora_contingencias';
        this.contingenciasActivas = new Map();
        this.brigadasConscientes = new Map();
        this.nichosMoviles = new Map();
    }
    
    // Activar protocolo de contingencia
    activarContingencia(tipoContingencia, ubicacion, parametros) {
        const contingencia = {
            id: this.generarIdContingencia(),
            tipo: tipoContingencia, // 'desastre_natural', 'crisis_comunitaria', 'emergencia_personal'
            ubicacion: ubicacion,
            timestamp_activacion: new Date().toISOString(),
            nivel_urgencia: parametros.urgencia || 'media',
            habitantes_convocados: [],
            nichos_desplegados: [],
            donaciones_activadas: 0,
            estado: 'activa'
        };
        
        // Convocar habitantes por resonancia
        this.convocarHabitantesPorResonancia(contingencia);
        
        // Desplegar nichos móviles
        this.desplegarNichosMoviles(contingencia);
        
        // Activar donaciones de emergencia
        this.activarDonacionesEmergencia(contingencia);
        
        this.contingenciasActivas.set(contingencia.id, contingencia);
        this.persistirContingencias();
        
        return contingencia;
    }
    
    convocarHabitantesPorResonancia(contingencia) {
        const habilidadesNecesarias = this.determinarHabilidadesNecesarias(contingencia.tipo);
        const habitantes = window.nichosServicio.habitantesOferentes;
        
        for (const [id, habitante] of habitantes) {
            if (habitante.disponibilidad === 'activa') {
                const resonancia = this.calcularResonanciaContingencia(
                    habitante.habilidades, 
                    habilidadesNecesarias
                );
                
                if (resonancia > 0.7) {
                    const convocatoria = {
                        habitante_id: id,
                        huella_servicio: habitante.huella_servicio,
                        resonancia: resonancia,
                        habilidades_relevantes: this.obtenerHabilidadesRelevantes(
                            habitante.habilidades, 
                            habilidadesNecesarias
                        ),
                        timestamp_convocatoria: new Date().toISOString(),
                        estado: 'convocado'
                    };
                    
                    contingencia.habitantes_convocados.push(convocatoria);
                    this.enviarConvocatoriaRitual(convocatoria, contingencia);
                }
            }
        }
    }
    
    determinarHabilidadesNecesarias(tipoContingencia) {
        const habilidadesPorTipo = {
            'desastre_natural': [
                'logística', 'distribución', 'acompañamiento', 'primeros auxilios',
                'coordinación', 'comunicación', 'traducción', 'orientación'
            ],
            'crisis_comunitaria': [
                'mediación', 'escucha', 'orientación legal', 'acompañamiento',
                'gestión recursos', 'comunicación', 'organización comunitaria'
            ],
            'emergencia_personal': [
                'escucha', 'acompañamiento emocional', 'orientación',
                'apoyo psicológico', 'gestión crisis', 'red de apoyo'
            ]
        };
        
        return habilidadesPorTipo[tipoContingencia] || ['acompañamiento', 'apoyo'];
    }
    
    calcularResonanciaContingencia(habilidadesHabitante, habilidadesNecesarias) {
        let coincidencias = 0;
        
        habilidadesHabitante.forEach(habilidad => {
            const descripcion = habilidad.descripcion.toLowerCase();
            habilidadesNecesarias.forEach(necesaria => {
                if (descripcion.includes(necesaria.toLowerCase())) {
                    coincidencias += 1;
                }
            });
        });
        
        return Math.min(coincidencias / habilidadesNecesarias.length, 1.0);
    }
    
    obtenerHabilidadesRelevantes(habilidades, necesarias) {
        return habilidades
            .filter(h => necesarias.some(n => 
                h.descripcion.toLowerCase().includes(n.toLowerCase())
            ))
            .map(h => h.huella);
    }
    
    enviarConvocatoriaRitual(convocatoria, contingencia) {
        // Registrar convocatoria en localStorage para que el habitante la vea
        const convocatorias = this.obtenerConvocatorias();
        convocatorias.push({
            id: `CONV-${Date.now().toString(36)}`,
            contingencia_id: contingencia.id,
            tipo_contingencia: contingencia.tipo,
            ubicacion: contingencia.ubicacion,
            urgencia: contingencia.nivel_urgencia,
            habilidades_solicitadas: convocatoria.habilidades_relevantes,
            timestamp: convocatoria.timestamp_convocatoria,
            estado: 'pendiente'
        });
        
        localStorage.setItem(`${this.clave}_convocatorias`, JSON.stringify(convocatorias));
    }
    
    // Desplegar nichos móviles de distribución
    desplegarNichosMoviles(contingencia) {
        const nichosNecesarios = this.determinarNichosNecesarios(contingencia.tipo);
        
        nichosNecesarios.forEach(tipoNicho => {
            const nicho = {
                id: this.generarIdNichoMovil(),
                tipo: tipoNicho,
                contingencia_id: contingencia.id,
                ubicacion: contingencia.ubicacion,
                timestamp_despliegue: new Date().toISOString(),
                recursos_disponibles: [],
                distribuciones_realizadas: 0,
                responsable_asignado: null,
                estado: 'desplegado'
            };
            
            this.nichosMoviles.set(nicho.id, nicho);
            contingencia.nichos_desplegados.push(nicho.id);
        });
    }
    
    determinarNichosNecesarios(tipoContingencia) {
        const nichosPorTipo = {
            'desastre_natural': ['distribucion_alimentos', 'acompañamiento_emocional', 'orientacion_legal'],
            'crisis_comunitaria': ['mediacion_conflictos', 'apoyo_psicosocial', 'gestion_recursos'],
            'emergencia_personal': ['escucha_activa', 'orientacion_crisis', 'red_apoyo']
        };
        
        return nichosPorTipo[tipoContingencia] || ['acompañamiento_general'];
    }
    
    // Activar donaciones de emergencia
    activarDonacionesEmergencia(contingencia) {
        const moduloEmergencia = {
            criterios_simplificados: true,
            verificacion_acelerada: true,
            distribucion_inmediata: true,
            trazabilidad_basica: true
        };
        
        // Registrar activación de donaciones de emergencia
        const activacion = {
            contingencia_id: contingencia.id,
            timestamp: new Date().toISOString(),
            modulo: moduloEmergencia,
            donaciones_recibidas: 0,
            distribuciones_realizadas: 0
        };
        
        localStorage.setItem(
            `${this.clave}_donaciones_emergencia_${contingencia.id}`, 
            JSON.stringify(activacion)
        );
        
        contingencia.donaciones_activadas = 1;
    }
    
    // Registrar necesidad de emergencia
    registrarNecesidadEmergencia(necesidad, ubicacion, urgencia) {
        const registro = {
            id: `NE-${Date.now().toString(36)}`,
            necesidad: necesidad,
            ubicacion: ubicacion,
            urgencia: urgencia, // 'critica', 'alta', 'media'
            timestamp: new Date().toISOString(),
            verificacion_simplificada: true,
            estado: 'activa',
            asignada_a_nicho: null
        };
        
        // Buscar nicho móvil más cercano
        const nichoAsignado = this.asignarNichoMasCercano(registro);
        if (nichoAsignado) {
            registro.asignada_a_nicho = nichoAsignado.id;
            nichoAsignado.recursos_disponibles.push(registro.id);
        }
        
        this.persistirNecesidadEmergencia(registro);
        return registro;
    }
    
    asignarNichoMasCercano(necesidad) {
        // Buscar nicho móvil en la misma ubicación
        for (const [id, nicho] of this.nichosMoviles) {
            if (nicho.ubicacion === necesidad.ubicacion && nicho.estado === 'desplegado') {
                return nicho;
            }
        }
        return null;
    }
    
    // Responder a convocatoria
    responderConvocatoria(convocatoriaId, respuesta, habitante) {
        const convocatorias = this.obtenerConvocatorias();
        const convocatoria = convocatorias.find(c => c.id === convocatoriaId);
        
        if (convocatoria && respuesta === 'acepto') {
            convocatoria.estado = 'aceptada';
            convocatoria.habitante_respondio = habitante.huella_consagracion;
            convocatoria.timestamp_respuesta = new Date().toISOString();
            
            // Asignar a nicho móvil
            this.asignarHabitanteANicho(convocatoria, habitante);
            
            localStorage.setItem(`${this.clave}_convocatorias`, JSON.stringify(convocatorias));
            
            return {
                mensaje: "Has sido asignado como brigada consciente.",
                nicho_asignado: convocatoria.nicho_asignado,
                instrucciones: this.generarInstruccionesRituales(convocatoria)
            };
        }
        
        return null;
    }
    
    asignarHabitanteANicho(convocatoria, habitante) {
        const contingencia = this.contingenciasActivas.get(convocatoria.contingencia_id);
        if (contingencia && contingencia.nichos_desplegados.length > 0) {
            const nichoId = contingencia.nichos_desplegados[0]; // Asignar al primer nicho disponible
            const nicho = this.nichosMoviles.get(nichoId);
            
            if (nicho && !nicho.responsable_asignado) {
                nicho.responsable_asignado = habitante.huella_consagracion;
                convocatoria.nicho_asignado = nichoId;
            }
        }
    }
    
    generarInstruccionesRituales(convocatoria) {
        return [
            "Mantén la presencia consciente en todo momento",
            "Reconoce la dignidad de cada persona que atiendas",
            "Distribuye desde el corazón, no desde el protocolo",
            "Registra cada gesto como acto de servicio consciente",
            "Recuerda: acompañas, no sustituyes"
        ];
    }
    
    // Métodos de utilidad
    generarIdContingencia() {
        return `CONT-${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 4)}`;
    }
    
    generarIdNichoMovil() {
        return `NM-${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 4)}`;
    }
    
    obtenerConvocatorias() {
        try {
            return JSON.parse(localStorage.getItem(`${this.clave}_convocatorias`) || '[]');
        } catch {
            return [];
        }
    }
    
    persistirContingencias() {
        const contingencias = Array.from(this.contingenciasActivas.entries());
        localStorage.setItem(`${this.clave}_activas`, JSON.stringify(contingencias));
    }
    
    persistirNecesidadEmergencia(necesidad) {
        const necesidades = this.obtenerNecesidadesEmergencia();
        necesidades.push(necesidad);
        localStorage.setItem(`${this.clave}_necesidades_emergencia`, JSON.stringify(necesidades));
    }
    
    obtenerNecesidadesEmergencia() {
        try {
            return JSON.parse(localStorage.getItem(`${this.clave}_necesidades_emergencia`) || '[]');
        } catch {
            return [];
        }
    }
    
    // Obtener estadísticas de contingencias
    obtenerEstadisticasContingencias() {
        return {
            contingencias_activas: this.contingenciasActivas.size,
            nichos_moviles_desplegados: this.nichosMoviles.size,
            habitantes_convocados: this.calcularHabitantesConvocados(),
            necesidades_emergencia: this.obtenerNecesidadesEmergencia().length,
            ultima_activacion: this.obtenerUltimaActivacion()
        };
    }
    
    calcularHabitantesConvocados() {
        let total = 0;
        for (const [id, contingencia] of this.contingenciasActivas) {
            total += contingencia.habitantes_convocados.length;
        }
        return total;
    }
    
    obtenerUltimaActivacion() {
        let ultimaFecha = null;
        for (const [id, contingencia] of this.contingenciasActivas) {
            if (!ultimaFecha || contingencia.timestamp_activacion > ultimaFecha) {
                ultimaFecha = contingencia.timestamp_activacion;
            }
        }
        return ultimaFecha;
    }
}

// Instancia global
window.protocoloContingencias = new ProtocoloContingencias();