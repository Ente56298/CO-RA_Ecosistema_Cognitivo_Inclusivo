// Componente Visual del Módulo de Servicio Consciente
class ModuloServicioVisual {
    constructor() {
        this.contenedor = null;
        this.guardian = window.guardianServicio;
        this.activo = false;
    }
    
    activar() {
        if (this.activo) return;
        this.activo = true;
        
        this.crearInterfaz();
        this.mostrarEstadoActual();
        this.configurarEventos();
    }
    
    crearInterfaz() {
        this.contenedor = document.createElement('div');
        this.contenedor.className = 'servicio-container';
        this.contenedor.innerHTML = `
            <div class="estado-consagracion" id="estado-consagracion"></div>
            
            <div class="guardian-mensaje" id="guardian-mensaje">
                ${this.guardian.iniciarDialogo()}
            </div>
            
            <input type="text" 
                   class="campo-servicio" 
                   id="campo-servicio"
                   placeholder="Escribe tu ofrecimiento..."
                   autocomplete="off"
                   spellcheck="false">
            
            <div class="huellas-flotantes" id="huellas-flotantes">
                <h4 style="color: #888; font-size: 0.8em; margin-bottom: 1rem; text-transform: uppercase; letter-spacing: 1px;">Huellas Flotantes</h4>
            </div>
            
            <div class="presencias-activas" id="presencias-activas">
                <h4 style="color: #888; font-size: 0.8em; margin-bottom: 1rem; text-transform: uppercase; letter-spacing: 1px;">Presencias Activas</h4>
            </div>
            
            <div class="coincidencia-revelada" id="coincidencia-revelada"></div>
            
            <div class="indicador-fase" id="indicador-fase">Fase: Ofrecimiento</div>
        `;
        
        document.body.appendChild(this.contenedor);
        
        // Activar animación de entrada
        setTimeout(() => {
            this.contenedor.classList.add('activo');
        }, 100);
    }
    
    mostrarEstadoActual() {
        const estado = this.guardian.obtenerEstado();
        const estadoElement = document.getElementById('estado-consagracion');
        
        let estadoHTML = '';
        if (estado.habitante_consciente) {
            estadoHTML += '<div class="habitante-consciente">Habitante Consciente</div>';
        }
        if (estado.sello_ritual) {
            estadoHTML += '<div class="sello-ritual">Sello Ritual Activado</div>';
        }
        
        estadoElement.innerHTML = estadoHTML;
        
        this.actualizarHuellasYPresencias();
    }
    
    actualizarHuellasYPresencias() {
        const registro = this.guardian.obtenerRegistro();
        
        // Mostrar últimas huellas flotantes
        const huellasContainer = document.getElementById('huellas-flotantes');
        const ofrecimientos = (registro.ofrecimientos || []).slice(-3);
        
        ofrecimientos.forEach((ofrecimiento, index) => {
            const huellaElement = document.createElement('div');
            huellaElement.className = 'huella-item';
            huellaElement.textContent = ofrecimiento.huella;
            huellasContainer.appendChild(huellaElement);
        });
        
        // Mostrar presencias activas
        const presenciasContainer = document.getElementById('presencias-activas');
        const necesidades = (registro.necesidades || []).slice(-3);
        
        necesidades.forEach((necesidad, index) => {
            const presenciaElement = document.createElement('div');
            presenciaElement.className = 'presencia-item';
            presenciaElement.textContent = necesidad.presencia;
            presenciasContainer.appendChild(presenciaElement);
        });
    }
    
    configurarEventos() {
        const campoServicio = document.getElementById('campo-servicio');
        const guardianMensaje = document.getElementById('guardian-mensaje');
        const indicadorFase = document.getElementById('indicador-fase');
        
        campoServicio.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                e.preventDefault();
                const texto = e.target.value.trim();
                if (texto) {
                    this.procesarEntrada(texto);
                }
            }
        });
    }
    
    procesarEntrada(texto) {
        const guardianMensaje = document.getElementById('guardian-mensaje');
        const campoServicio = document.getElementById('campo-servicio');
        const indicadorFase = document.getElementById('indicador-fase');
        
        let respuesta;
        
        if (this.guardian.fase === 'inicial') {
            respuesta = this.guardian.procesarOfrecimiento(texto);
            this.agregarHuellaFlotante(texto);
            
            if (this.guardian.fase === 'necesidad') {
                campoServicio.placeholder = "Escribe tu necesidad...";
                indicadorFase.textContent = "Fase: Necesidad";
            }
        } else if (this.guardian.fase === 'necesidad') {
            respuesta = this.guardian.procesarNecesidad(texto);
            this.agregarPresenciaActiva(texto);
            
            // Verificar si hay coincidencias
            if (respuesta.includes('Alguien ofreció')) {
                this.mostrarCoincidencia(respuesta);
                return;
            }
            
            indicadorFase.textContent = "Fase: Revelación";
        }
        
        // Actualizar mensaje del guardián
        guardianMensaje.textContent = respuesta;
        campoServicio.value = '';
        
        // Actualizar estado de consagración
        this.actualizarEstadoConsagracion();
    }
    
    agregarHuellaFlotante(texto) {
        const huellasContainer = document.getElementById('huellas-flotantes');
        const huellaElement = document.createElement('div');
        huellaElement.className = 'huella-item';
        huellaElement.textContent = this.guardian.crearHuellaFlotante(texto);
        huellaElement.style.animationDelay = '0s';
        huellasContainer.appendChild(huellaElement);
    }
    
    agregarPresenciaActiva(texto) {
        const presenciasContainer = document.getElementById('presencias-activas');
        const presenciaElement = document.createElement('div');
        presenciaElement.className = 'presencia-item';
        presenciaElement.textContent = this.guardian.crearPresenciaActiva(texto);
        presenciaElement.style.animationDelay = '0s';
        presenciasContainer.appendChild(presenciaElement);
    }
    
    mostrarCoincidencia(mensaje) {
        const coincidenciaContainer = document.getElementById('coincidencia-revelada');
        coincidenciaContainer.innerHTML = `
            <div class="coincidencia-texto">${mensaje}</div>
            <button class="boton-señal" onclick="moduloServicioVisual.dejarSeñal()">
                Dejar una señal
            </button>
        `;
        
        setTimeout(() => {
            coincidenciaContainer.classList.add('mostrar');
        }, 500);
    }
    
    dejarSeñal() {
        const mensaje = prompt('¿Qué señal quieres dejar?');
        if (mensaje && mensaje.trim()) {
            const respuesta = this.guardian.dejarSeñal(mensaje.trim());
            
            const guardianMensaje = document.getElementById('guardian-mensaje');
            guardianMensaje.textContent = respuesta;
            
            const coincidenciaContainer = document.getElementById('coincidencia-revelada');
            coincidenciaContainer.classList.remove('mostrar');
            
            this.actualizarEstadoConsagracion();
        }
    }
    
    actualizarEstadoConsagracion() {
        const estado = this.guardian.obtenerEstado();
        const estadoElement = document.getElementById('estado-consagracion');
        
        let estadoHTML = '';
        if (estado.habitante_consciente) {
            estadoHTML += '<div class="habitante-consciente">Habitante Consciente</div>';
        }
        if (estado.sello_ritual) {
            estadoHTML += '<div class="sello-ritual">Sello Ritual Activado</div>';
        }
        
        estadoElement.innerHTML = estadoHTML;
    }
    
    desactivar() {
        if (this.contenedor) {
            this.contenedor.classList.remove('activo');
            setTimeout(() => {
                document.body.removeChild(this.contenedor);
                this.contenedor = null;
                this.activo = false;
            }, 1000);
        }
    }
}

// Instancia global
window.moduloServicioVisual = new ModuloServicioVisual();