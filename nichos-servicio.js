// Sistema de Nichos Rituales de Servicio - CO•RA
class NichosServicio {
    constructor() {
        this.clave = 'cora_nichos_servicio';
        this.nichosActivos = new Map();
        this.habitantesOferentes = new Map();
    }
    
    // Registrar habitante como oferente consciente
    registrarOferente(habitante, habilidades) {
        const oferente = {
            id: this.generarIdOferente(),
            timestamp: new Date().toISOString(),
            habilidades: habilidades.map(h => this.procesarHabilidad(h)),
            disponibilidad: 'activa',
            huella_servicio: this.generarHuellaServicio(habilidades),
            verificado: this.verificarHabitante(habitante),
            nicho_asignado: this.asignarNicho(habilidades)
        };
        
        if (oferente.verificado) {
            this.habitantesOferentes.set(oferente.id, oferente);
            this.actualizarNicho(oferente.nicho_asignado, oferente);
            this.persistirOferentes();
            return oferente;
        }
        
        return null;
    }
    
    procesarHabilidad(habilidad) {
        return {
            descripcion: habilidad.trim(),
            categoria: this.categorizarHabilidad(habilidad),
            huella: this.crearHuellaHabilidad(habilidad),
            verificada: this.verificarHabilidad(habilidad)
        };
    }
    
    categorizarHabilidad(habilidad) {
        const categorias = {
            'acompañamiento': ['escuchar', 'acompañar', 'sostener', 'cuidar', 'presencia'],
            'enseñanza': ['enseñar', 'explicar', 'guiar', 'mostrar', 'educar'],
            'técnico': ['programar', 'diseñar', 'desarrollar', 'crear', 'construir'],
            'cuidado': ['sanar', 'proteger', 'ayudar', 'asistir', 'apoyar'],
            'creativo': ['arte', 'música', 'escribir', 'crear', 'imaginar']
        };
        
        const habilidadLower = habilidad.toLowerCase();
        
        for (const [categoria, palabras] of Object.entries(categorias)) {
            if (palabras.some(palabra => habilidadLower.includes(palabra))) {
                return categoria;
            }
        }
        
        return 'general';
    }
    
    crearHuellaHabilidad(habilidad) {
        const palabrasClave = habilidad.split(' ')
            .filter(p => p.length > 3)
            .slice(0, 2)
            .join(' ');
        return `${palabrasClave}...`;
    }
    
    verificarHabilidad(habilidad) {
        return habilidad.length > 10 && 
               habilidad.split(' ').length >= 2 &&
               !['test', 'prueba', 'demo'].some(p => habilidad.toLowerCase().includes(p));
    }
    
    verificarHabitante(habitante) {
        return habitante.habitante_consciente && 
               habitante.ofrecimientos_verificados > 0;
    }
    
    asignarNicho(habilidades) {
        const categorias = habilidades.map(h => h.categoria);
        const categoriaPrincipal = this.obtenerCategoriaPrincipal(categorias);
        return `nicho_${categoriaPrincipal}`;
    }
    
    obtenerCategoriaPrincipal(categorias) {
        const conteo = {};
        categorias.forEach(cat => {
            conteo[cat] = (conteo[cat] || 0) + 1;
        });
        
        return Object.keys(conteo).reduce((a, b) => 
            conteo[a] > conteo[b] ? a : b
        );
    }
    
    generarIdOferente() {
        return `OF-${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 6)}`;
    }
    
    generarHuellaServicio(habilidades) {
        const resumen = habilidades.slice(0, 3).map(h => h.slice(0, 5)).join('-');
        return `HS-${resumen}-${Date.now().toString(36).slice(-4)}`;
    }
    
    // Buscar oferentes para necesidad específica
    buscarOferentes(necesidad) {
        const necesidadProcesada = this.procesarNecesidad(necesidad);
        const oferentesCompatibles = [];
        
        for (const [id, oferente] of this.habitantesOferentes) {
            if (oferente.disponibilidad === 'activa') {
                const compatibilidad = this.calcularCompatibilidad(
                    necesidadProcesada, 
                    oferente.habilidades
                );
                
                if (compatibilidad > 0.6) {
                    oferentesCompatibles.push({
                        id: oferente.id,
                        huella_servicio: oferente.huella_servicio,
                        compatibilidad: compatibilidad,
                        habilidades_relevantes: this.obtenerHabilidadesRelevantes(
                            necesidadProcesada, 
                            oferente.habilidades
                        )
                    });
                }
            }
        }
        
        return oferentesCompatibles.sort((a, b) => b.compatibilidad - a.compatibilidad);
    }
    
    procesarNecesidad(necesidad) {
        return {
            descripcion: necesidad.trim(),
            categoria: this.categorizarHabilidad(necesidad),
            palabras_clave: this.extraerPalabrasClave(necesidad)
        };
    }
    
    extraerPalabrasClave(texto) {
        return texto.toLowerCase()
            .split(' ')
            .filter(p => p.length > 3)
            .slice(0, 5);
    }
    
    calcularCompatibilidad(necesidad, habilidades) {
        let puntuacion = 0;
        
        // Compatibilidad por categoría
        const habilidadesMismaCategoria = habilidades.filter(h => 
            h.categoria === necesidad.categoria
        );
        if (habilidadesMismaCategoria.length > 0) {
            puntuacion += 0.4;
        }
        
        // Compatibilidad semántica
        const coincidenciasPalabras = necesidad.palabras_clave.filter(palabra =>
            habilidades.some(h => h.descripcion.toLowerCase().includes(palabra))
        );
        puntuacion += (coincidenciasPalabras.length / necesidad.palabras_clave.length) * 0.6;
        
        return Math.min(puntuacion, 1.0);
    }
    
    obtenerHabilidadesRelevantes(necesidad, habilidades) {
        return habilidades
            .filter(h => h.categoria === necesidad.categoria)
            .map(h => h.huella)
            .slice(0, 2);
    }
    
    // Crear oficina simbólica de distribución
    crearOficinaSimbolica(ubicacion, responsable) {
        const oficina = {
            id: this.generarIdOficina(),
            ubicacion: ubicacion,
            responsable_huella: responsable.huella_consagracion,
            timestamp_creacion: new Date().toISOString(),
            oferentes_asociados: [],
            activaciones_realizadas: 0,
            estado: 'activa'
        };
        
        this.registrarOficina(oficina);
        return oficina;
    }
    
    generarIdOficina() {
        return `OSI-${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 4)}`;
    }
    
    // Activar servicio desde oficina
    activarDesdeOficina(oficinaId, tipoActivacion) {
        const oficina = this.obtenerOficina(oficinaId);
        if (!oficina) return null;
        
        const activacion = {
            timestamp: new Date().toISOString(),
            oficina_id: oficinaId,
            tipo: tipoActivacion, // 'qr', 'tarjeta', 'presencial'
            codigo_activacion: this.generarCodigoActivacion()
        };
        
        oficina.activaciones_realizadas += 1;
        this.actualizarOficina(oficina);
        
        return {
            mensaje: "CO•RA te reconoce desde este espacio de servicio.",
            codigo: activacion.codigo_activacion,
            url_umbral: `${window.location.origin}?activacion=${activacion.codigo_activacion}`
        };
    }
    
    generarCodigoActivacion() {
        return `ACT-${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 6)}`;
    }
    
    // Obtener mapa de nichos activos
    obtenerMapaNichos() {
        const mapa = {
            timestamp: new Date().toISOString(),
            nichos_activos: {},
            total_oferentes: this.habitantesOferentes.size,
            oficinas_simbolicas: this.obtenerOficinasActivas().length
        };
        
        // Agrupar oferentes por nicho
        for (const [id, oferente] of this.habitantesOferentes) {
            if (oferente.disponibilidad === 'activa') {
                const nicho = oferente.nicho_asignado;
                if (!mapa.nichos_activos[nicho]) {
                    mapa.nichos_activos[nicho] = {
                        oferentes: 0,
                        habilidades_disponibles: [],
                        ultima_actividad: null
                    };
                }
                
                mapa.nichos_activos[nicho].oferentes += 1;
                mapa.nichos_activos[nicho].habilidades_disponibles.push(
                    ...oferente.habilidades.map(h => h.huella)
                );
                mapa.nichos_activos[nicho].ultima_actividad = oferente.timestamp;
            }
        }
        
        return mapa;
    }
    
    // Métodos de persistencia
    persistirOferentes() {
        const oferentes = Array.from(this.habitantesOferentes.entries());
        localStorage.setItem(`${this.clave}_oferentes`, JSON.stringify(oferentes));
    }
    
    cargarOferentes() {
        try {
            const oferentes = JSON.parse(localStorage.getItem(`${this.clave}_oferentes`) || '[]');
            this.habitantesOferentes = new Map(oferentes);
        } catch {
            this.habitantesOferentes = new Map();
        }
    }
    
    registrarOficina(oficina) {
        const oficinas = this.obtenerOficinas();
        oficinas.push(oficina);
        localStorage.setItem(`${this.clave}_oficinas`, JSON.stringify(oficinas));
    }
    
    obtenerOficinas() {
        try {
            return JSON.parse(localStorage.getItem(`${this.clave}_oficinas`) || '[]');
        } catch {
            return [];
        }
    }
    
    obtenerOficina(id) {
        return this.obtenerOficinas().find(o => o.id === id);
    }
    
    obtenerOficinasActivas() {
        return this.obtenerOficinas().filter(o => o.estado === 'activa');
    }
    
    actualizarOficina(oficina) {
        const oficinas = this.obtenerOficinas();
        const index = oficinas.findIndex(o => o.id === oficina.id);
        if (index !== -1) {
            oficinas[index] = oficina;
            localStorage.setItem(`${this.clave}_oficinas`, JSON.stringify(oficinas));
        }
    }
    
    actualizarNicho(nichoId, oferente) {
        // Actualizar estadísticas del nicho
        const nichos = this.obtenerEstadisticasNichos();
        if (!nichos[nichoId]) {
            nichos[nichoId] = { oferentes: 0, ultima_actualizacion: null };
        }
        nichos[nichoId].oferentes += 1;
        nichos[nichoId].ultima_actualizacion = new Date().toISOString();
        
        localStorage.setItem(`${this.clave}_nichos`, JSON.stringify(nichos));
    }
    
    obtenerEstadisticasNichos() {
        try {
            return JSON.parse(localStorage.getItem(`${this.clave}_nichos`) || '{}');
        } catch {
            return {};
        }
    }
}

// Instancia global
window.nichosServicio = new NichosServicio();

// Cargar datos al inicializar
window.nichosServicio.cargarOferentes();