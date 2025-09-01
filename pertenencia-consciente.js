// Módulo de Pertenencia Consciente - Registro post-vacío
class PertenenciaConsciente {
    constructor() {
        this.clave = 'cora_habitante_reconocido';
    }
    
    mostrarInvitacionPertenencia() {
        const constancia = window.constanciaRitual.evaluarConstancia();
        
        // Solo mostrar si ha demostrado intención auténtica
        if (constancia.nivel === 'primera_manifestacion' || 
            constancia.nivel === 'regreso_consciente') {
            return;
        }
        
        this.crearFormularioPertenencia();
    }
    
    crearFormularioPertenencia() {
        const formulario = document.createElement('div');
        formulario.className = 'formulario-pertenencia';
        formulario.innerHTML = `
            <div class="invitacion-pertenencia">
                ¿Deseas ser parte de CO•RA?
            </div>
            
            <div class="campo-grupo">
                <label for="nombre-simbolico">Nombre simbólico:</label>
                <input type="text" id="nombre-simbolico" 
                       placeholder="Cómo quieres ser reconocido aquí"
                       maxlength="30">
            </div>
            
            <div class="campo-grupo">
                <label for="intencion-personal">Tu intención:</label>
                <textarea id="intencion-personal" 
                          placeholder="Una frase que te represente en este espacio"
                          maxlength="150"></textarea>
            </div>
            
            <div class="campo-grupo">
                <label>Tu compromiso:</label>
                <div class="opciones-compromiso">
                    <label><input type="radio" name="compromiso" value="servir"> Servir</label>
                    <label><input type="radio" name="compromiso" value="acompañar"> Acompañar</label>
                    <label><input type="radio" name="compromiso" value="construir"> Construir</label>
                </div>
            </div>
            
            <div class="acciones-pertenencia">
                <button id="confirmar-pertenencia">Confirmar intención</button>
                <button id="continuar-sin-registro">Continuar sin registrar</button>
            </div>
        `;
        
        // Estilos
        formulario.style.cssText = `
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: rgba(255,255,255,0.95);
            padding: 2rem;
            border-radius: 8px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            max-width: 400px;
            width: 90vw;
            z-index: 1000;
            font-family: 'Helvetica Neue', Arial, sans-serif;
            color: #333;
        `;
        
        document.body.appendChild(formulario);
        this.configurarEventos(formulario);
    }
    
    configurarEventos(formulario) {
        const confirmar = formulario.querySelector('#confirmar-pertenencia');
        const continuar = formulario.querySelector('#continuar-sin-registro');
        
        confirmar.addEventListener('click', () => {
            this.procesarRegistro(formulario);
        });
        
        continuar.addEventListener('click', () => {
            this.continuarSinRegistro(formulario);
        });
    }
    
    procesarRegistro(formulario) {
        const nombre = formulario.querySelector('#nombre-simbolico').value.trim();
        const intencion = formulario.querySelector('#intencion-personal').value.trim();
        const compromiso = formulario.querySelector('input[name="compromiso"]:checked')?.value;
        
        if (!nombre || !intencion || !compromiso) {
            this.mostrarMensaje('Completa todos los campos para confirmar tu intención.');
            return;
        }
        
        const habitante = {
            nombre_simbolico: nombre,
            intencion_personal: intencion,
            compromiso: compromiso,
            timestamp_reconocimiento: new Date().toISOString(),
            nivel_constancia: window.constanciaRitual.evaluarConstancia().nivel,
            presencia_confirmada: true
        };
        
        localStorage.setItem(this.clave, JSON.stringify(habitante));
        
        // Registrar en bitácora
        window.bitacora.registrarEvento('habitante_reconocido', habitante);
        
        this.mostrarConfirmacion(formulario, habitante);
    }
    
    continuarSinRegistro(formulario) {
        formulario.remove();
        this.mostrarMensaje('Puedes registrarte cuando sientas que es el momento.', 3000);
    }
    
    mostrarConfirmacion(formulario, habitante) {
        formulario.innerHTML = `
            <div class="confirmacion-pertenencia">
                <h3>Bienvenido, ${habitante.nombre_simbolico}</h3>
                <p>Tu intención ha sido reconocida:</p>
                <blockquote>"${habitante.intencion_personal}"</blockquote>
                <p>Compromiso: <strong>${habitante.compromiso}</strong></p>
                <button id="ingresar-ecosistema">Ingresar al ecosistema</button>
            </div>
        `;
        
        formulario.querySelector('#ingresar-ecosistema').addEventListener('click', () => {
            formulario.remove();
            this.activarEcosistema();
        });
    }
    
    activarEcosistema() {
        // Revelar módulos del núcleo
        this.mostrarMensaje('El ecosistema CO•RA se revela para ti...', 2000);
        
        setTimeout(() => {
            // Aquí se activarían los módulos del núcleo
            window.location.href = 'nucleo-cora.html';
        }, 2000);
    }
    
    mostrarMensaje(texto, duracion = 5000) {
        const mensaje = document.createElement('div');
        mensaje.textContent = texto;
        mensaje.style.cssText = `
            position: fixed;
            top: 20px;
            left: 50%;
            transform: translateX(-50%);
            background: rgba(0,0,0,0.8);
            color: white;
            padding: 1rem 2rem;
            border-radius: 4px;
            z-index: 1001;
            font-size: 0.9em;
        `;
        
        document.body.appendChild(mensaje);
        
        setTimeout(() => {
            mensaje.remove();
        }, duracion);
    }
    
    esHabitanteReconocido() {
        const habitante = localStorage.getItem(this.clave);
        return habitante !== null;
    }
    
    obtenerHabitante() {
        const habitante = localStorage.getItem(this.clave);
        return habitante ? JSON.parse(habitante) : null;
    }
}

// Instancia global
window.pertenenciaConsciente = new PertenenciaConsciente();