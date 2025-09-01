// Ciudad CO•RA - Portal Comunitario del Despertar
class CiudadCORA {
    constructor() {
        this.clave = 'cora_ciudad_portal';
        this.biblioteca = new BibliotecaViva();
        this.nucleo = new NucleoManifestacion();
        this.espaciosRituales = new Map();
        this.presenciasActivas = new Map();
    }
    
    // Inicializar la ciudad
    inicializarCiudad() {
        const ciudad = {
            id: 'CIUDAD-CORA-PRINCIPAL',
            timestamp_creacion: new Date().toISOString(),
            centro: this.biblioteca.inicializar(),
            nucleo: this.nucleo.inicializar(),
            espacios_rituales: [],
            habitantes_activos: 0,
            ecos_flotantes: 0,
            estado: 'activa'
        };
        
        this.persistirCiudad(ciudad);
        return ciudad;
    }
    
    // Crear espacio ritual para habitante
    crearEspacioRitual(habitante, tipoEspacio) {
        if (!habitante.habitante_consciente) {
            return null;
        }
        
        const espacio = {
            id: this.generarIdEspacio(),
            propietario_huella: habitante.huella_consagracion,
            tipo: tipoEspacio, // 'oficina_simbolica', 'nicho_ayuda', 'altar_habilidades'
            timestamp_creacion: new Date().toISOString(),
            habilidades_ofrecidas: this.extraerHabilidades(habitante),
            visitantes_atendidos: 0,
            ecos_generados: 0,
            estado: 'activo'
        };
        
        this.espaciosRituales.set(espacio.id, espacio);
        this.persistirEspacios();
        
        return espacio;
    }
    
    extraerHabilidades(habitante) {
        const registro = window.guardianServicio.obtenerRegistro();
        return (registro.ofrecimientos || [])
            .filter(o => o.verificado)
            .map(o => o.huella)
            .slice(0, 5);
    }
    
    // Registrar presencia en la ciudad
    registrarPresencia(visitante, ubicacion) {
        const presencia = {
            id: this.generarIdPresencia(),
            timestamp: new Date().toISOString(),
            ubicacion: ubicacion, // 'biblioteca', 'nucleo', 'espacio_ritual'
            tipo_visitante: this.determinarTipoVisitante(visitante),
            intencion_detectada: this.detectarIntencion(visitante),
            duracion_visita: 0,
            ecos_dejados: []
        };
        
        this.presenciasActivas.set(presencia.id, presencia);
        
        // Actualizar estadísticas de la ciudad
        this.actualizarEstadisticasCiudad();
        
        return presencia;
    }
    
    determinarTipoVisitante(visitante) {
        if (visitante.habitante_consciente) {
            return visitante.sello_ritual ? 'habitante_consagrado' : 'habitante_consciente';
        }
        return 'visitante_inicial';
    }
    
    detectarIntencion(visitante) {
        const estado = window.guardianServicio.obtenerEstado();
        
        if (estado.ofrecimientos_verificados > 0) {
            return 'servicio';
        } else if (estado.necesidades_verificadas > 0) {
            return 'necesidad';
        } else {
            return 'exploracion';
        }
    }
    
    // Generar eco flotante en la biblioteca
    generarEcoFlotante(texto, ubicacion, autor) {
        const eco = {
            id: this.generarIdEco(),
            texto_huella: this.crearHuellaTexto(texto),
            ubicacion_origen: ubicacion,
            autor_huella: autor.huella_consagracion || 'anonimo',
            timestamp: new Date().toISOString(),
            resonancia: this.calcularResonancia(texto),
            visto_por: [],
            estado: 'flotante'
        };
        
        this.biblioteca.agregarEco(eco);
        return eco;
    }
    
    crearHuellaTexto(texto) {
        const palabrasClave = texto.split(' ')
            .filter(p => p.length > 3)
            .slice(0, 4)
            .join(' ');
        return `${palabrasClave}...`;
    }
    
    calcularResonancia(texto) {
        const palabrasResonantes = [
            'ayuda', 'acompañar', 'servir', 'sostener', 'cuidar',
            'necesito', 'busco', 'ofrezco', 'puedo', 'quiero'
        ];
        
        let resonancia = 0;
        palabrasResonantes.forEach(palabra => {
            if (texto.toLowerCase().includes(palabra)) {
                resonancia += 0.2;
            }
        });
        
        return Math.min(resonancia, 1.0);
    }
    
    // Activar núcleo por intención colectiva
    activarNucleoPorIntencion() {
        const intenciones = Array.from(this.presenciasActivas.values())
            .map(p => p.intencion_detectada);
        
        const intencionesServicio = intenciones.filter(i => i === 'servicio').length;
        const totalPresencias = intenciones.length;
        
        if (totalPresencias > 0 && (intencionesServicio / totalPresencias) > 0.6) {
            return this.nucleo.activarPorServicioColectivo();
        }
        
        return false;
    }
    
    // Obtener mapa de presencias para la biblioteca
    obtenerMapaPresencias() {
        const mapa = {
            timestamp: new Date().toISOString(),
            presencias_activas: this.presenciasActivas.size,
            espacios_rituales: this.espaciosRituales.size,
            ecos_flotantes: this.biblioteca.obtenerConteoEcos(),
            nucleo_estado: this.nucleo.obtenerEstado(),
            distribución_por_ubicacion: this.calcularDistribucionUbicaciones(),
            intenciones_detectadas: this.calcularDistribucionIntenciones()
        };
        
        return mapa;
    }
    
    calcularDistribucionUbicaciones() {
        const distribucion = {};
        
        for (const [id, presencia] of this.presenciasActivas) {
            const ubicacion = presencia.ubicacion;
            distribucion[ubicacion] = (distribucion[ubicacion] || 0) + 1;
        }
        
        return distribucion;
    }
    
    calcularDistribucionIntenciones() {
        const distribucion = {};
        
        for (const [id, presencia] of this.presenciasActivas) {
            const intencion = presencia.intencion_detectada;
            distribucion[intencion] = (distribucion[intencion] || 0) + 1;
        }
        
        return distribucion;
    }
    
    // Buscar coincidencias en la ciudad
    buscarCoincidenciasEnCiudad(necesidad) {
        const coincidencias = [];
        
        // Buscar en espacios rituales
        for (const [id, espacio] of this.espaciosRituales) {
            if (espacio.estado === 'activo') {
                const compatibilidad = this.evaluarCompatibilidadEspacio(necesidad, espacio);
                if (compatibilidad > 0.6) {
                    coincidencias.push({
                        tipo: 'espacio_ritual',
                        id: espacio.id,
                        compatibilidad: compatibilidad,
                        habilidades: espacio.habilidades_ofrecidas
                    });
                }
            }
        }
        
        // Buscar en ecos flotantes
        const ecosRelevantes = this.biblioteca.buscarEcosRelevantes(necesidad);
        coincidencias.push(...ecosRelevantes);
        
        return coincidencias.sort((a, b) => b.compatibilidad - a.compatibilidad);
    }
    
    evaluarCompatibilidadEspacio(necesidad, espacio) {
        const necesidadLower = necesidad.toLowerCase();
        let compatibilidad = 0;
        
        espacio.habilidades_ofrecidas.forEach(habilidad => {
            if (necesidadLower.includes(habilidad.toLowerCase().slice(0, 5))) {
                compatibilidad += 0.3;
            }
        });
        
        return Math.min(compatibilidad, 1.0);
    }
    
    // Métodos de utilidad
    generarIdEspacio() {
        return `ESP-${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 4)}`;
    }
    
    generarIdPresencia() {
        return `PRES-${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 4)}`;
    }
    
    generarIdEco() {
        return `ECO-${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 4)}`;
    }
    
    actualizarEstadisticasCiudad() {
        const estadisticas = {
            timestamp: new Date().toISOString(),
            presencias_totales: this.presenciasActivas.size,
            espacios_activos: Array.from(this.espaciosRituales.values())
                .filter(e => e.estado === 'activo').length,
            ecos_generados: this.biblioteca.obtenerConteoEcos(),
            activaciones_nucleo: this.nucleo.obtenerActivaciones()
        };
        
        localStorage.setItem(`${this.clave}_estadisticas`, JSON.stringify(estadisticas));
    }
    
    persistirCiudad(ciudad) {
        localStorage.setItem(`${this.clave}_principal`, JSON.stringify(ciudad));
    }
    
    persistirEspacios() {
        const espacios = Array.from(this.espaciosRituales.entries());
        localStorage.setItem(`${this.clave}_espacios`, JSON.stringify(espacios));
    }
    
    obtenerEstadisticasCiudad() {
        try {
            return JSON.parse(localStorage.getItem(`${this.clave}_estadisticas`) || '{}');
        } catch {
            return {};
        }
    }
}

// Biblioteca Viva - Memoria colectiva de la ciudad
class BibliotecaViva {
    constructor() {
        this.ecos = new Map();
        this.memoriaColectiva = [];
    }
    
    inicializar() {
        return {
            id: 'BIBLIOTECA-VIVA-CENTRAL',
            ecos_flotantes: 0,
            memoria_colectiva: 0,
            visitantes_diarios: 0,
            resonancia_promedio: 0
        };
    }
    
    agregarEco(eco) {
        this.ecos.set(eco.id, eco);
        this.memoriaColectiva.push({
            timestamp: eco.timestamp,
            huella: eco.texto_huella,
            resonancia: eco.resonancia
        });
        
        // Mantener solo últimos 1000 ecos
        if (this.memoriaColectiva.length > 1000) {
            this.memoriaColectiva.shift();
        }
        
        this.persistirBiblioteca();
    }
    
    buscarEcosRelevantes(consulta) {
        const consultaLower = consulta.toLowerCase();
        const ecosRelevantes = [];
        
        for (const [id, eco] of this.ecos) {
            if (eco.texto_huella.toLowerCase().includes(consultaLower.slice(0, 10))) {
                ecosRelevantes.push({
                    tipo: 'eco_flotante',
                    id: eco.id,
                    compatibilidad: eco.resonancia,
                    huella: eco.texto_huella
                });
            }
        }
        
        return ecosRelevantes;
    }
    
    obtenerConteoEcos() {
        return this.ecos.size;
    }
    
    persistirBiblioteca() {
        const biblioteca = {
            ecos: Array.from(this.ecos.entries()),
            memoria: this.memoriaColectiva
        };
        localStorage.setItem('cora_biblioteca_viva', JSON.stringify(biblioteca));
    }
}

// Núcleo de Manifestación - Sensor de intención colectiva
class NucleoManifestacion {
    constructor() {
        this.activaciones = 0;
        this.ultimaActivacion = null;
        this.intencionColectiva = 0;
    }
    
    inicializar() {
        return {
            id: 'NUCLEO-MANIFESTACION-CENTRAL',
            estado: 'latente',
            activaciones_totales: 0,
            intencion_colectiva: 0,
            ultima_activacion: null
        };
    }
    
    activarPorServicioColectivo() {
        this.activaciones += 1;
        this.ultimaActivacion = new Date().toISOString();
        this.intencionColectiva = this.calcularIntencionColectiva();
        
        this.persistirNucleo();
        
        return {
            activado: true,
            mensaje: "El núcleo se revela por servicio colectivo",
            intencion_colectiva: this.intencionColectiva
        };
    }
    
    calcularIntencionColectiva() {
        // Calcular basado en actividad reciente
        const ahora = new Date();
        const hace24h = new Date(ahora - 24 * 60 * 60 * 1000);
        
        // Simulación de cálculo de intención colectiva
        return Math.min(this.activaciones * 0.1, 1.0);
    }
    
    obtenerEstado() {
        return {
            activaciones: this.activaciones,
            ultima_activacion: this.ultimaActivacion,
            intencion_colectiva: this.intencionColectiva,
            estado: this.intencionColectiva > 0.5 ? 'activo' : 'latente'
        };
    }
    
    obtenerActivaciones() {
        return this.activaciones;
    }
    
    persistirNucleo() {
        const nucleo = {
            activaciones: this.activaciones,
            ultima_activacion: this.ultimaActivacion,
            intencion_colectiva: this.intencionColectiva
        };
        localStorage.setItem('cora_nucleo_manifestacion', JSON.stringify(nucleo));
    }
}

// Instancia global
window.ciudadCORA = new CiudadCORA();