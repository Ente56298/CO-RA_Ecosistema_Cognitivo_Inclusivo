const intencion = document.getElementById('intencion');
const punto = document.getElementById('punto');
const cuestionamiento = document.getElementById('cuestionamiento');

let secuenciaIniciada = false;

const palabrasResonantes = [
    'ayuda', 'acompañar', 'entender', 'escuchar', 'comprender',
    'incluir', 'accesible', 'familia', 'aprender', 'crecer',
    'colaborar', 'juntos', 'diversidad', 'respeto', 'empatía',
    'cuidar', 'proteger', 'sanar', 'transformar', 'evolucionar',
    'necesito', 'busco', 'quiero', 'siento', 'espero', 'dolor',
    'solo', 'perdido', 'confundido', 'miedo', 'esperanza'
];

intencion.addEventListener('input', function(e) {
    const texto = e.target.value.toLowerCase().trim();
    
    // Modo servicio activo
    if (window.modoServicio) {
        return; // El manejo se hace en el submit
    }
    
    if (texto.length > 4 && !secuenciaIniciada) {
        const tieneResonancia = palabrasResonantes.some(palabra => 
            texto.includes(palabra)
        );
        
        const tieneAutenticidad = texto.length > 10 && 
                                !texto.includes('test') && 
                                !texto.includes('hola') &&
                                !texto.includes('demo') &&
                                !texto.includes('prueba') &&
                                texto.split(' ').length > 2;
        
        if (tieneResonancia || tieneAutenticidad) {
            activarSecuencia(texto);
        }
    }
});

// Manejar diálogo de servicio
intencion.addEventListener('keypress', function(e) {
    if (e.key === 'Enter' && window.modoServicio) {
        e.preventDefault();
        const texto = e.target.value.trim();
        if (texto) {
            procesarDialogoServicio(texto);
        }
    }
});

function procesarDialogoServicio(texto) {
    const guardian = window.guardianServicio;
    let respuesta;
    
    if (guardian.fase === 'inicial') {
        respuesta = guardian.procesarOfrecimiento(texto);
    } else if (guardian.fase === 'necesidad') {
        respuesta = guardian.procesarNecesidad(texto);
    }
    
    // Mostrar respuesta del guardián
    cuestionamiento.innerHTML = respuesta;
    
    // Limpiar campo
    intencion.value = "";
    
    // Actualizar placeholder según fase
    if (guardian.fase === 'necesidad') {
        intencion.placeholder = "Escribe tu necesidad...";
    } else {
        intencion.placeholder = "Continúa el diálogo...";
    }
}

function activarSecuencia(textoIntencion) {
    if (secuenciaIniciada) return;
    secuenciaIniciada = true;
    
    // Registrar escritura en sistema de constancia
    window.constanciaRitual.registrarEscritura(textoIntencion);
    
    // Registrar en bitácora silenciosa
    window.bitacora.registrarUmbral(textoIntencion);
    
    localStorage.setItem('cora_umbral_cruzado', JSON.stringify({
        timestamp: new Date().toISOString(),
        intencion: textoIntencion,
        dominio: 'CO-RA.ecosistema.mx',
        ritual_completado: true
    }));
    
    // Vibración del entorno - el blanco respira
    document.body.classList.add('vibrar');
    
    // Suspender cursor
    intencion.style.caretColor = 'transparent';
    
    setTimeout(() => {
        // Manifestación del punto desde el fondo
        punto.classList.add('manifestacion-punto');
        punto.style.opacity = '1';
        
        setTimeout(() => {
            cuestionamiento.style.opacity = '1';
            cuestionamiento.setAttribute('aria-live', 'assertive');
        }, 4000);
    }, 2000);
}

punto.addEventListener('click', function() {
    if (secuenciaIniciada) {
        const constancia = window.constanciaRitual.evaluarConstancia();
        
        punto.style.transform = 'translate(-50%, -50%) scale(0)';
        setTimeout(() => {
            // Activar módulo visual de servicio
            window.moduloServicioVisual.activar();
            
            // Verificar si puede ser registrado como oferente
            setTimeout(() => {
                const estado = window.guardianServicio.obtenerEstado();
                if (estado.habitante_consciente && estado.ofrecimientos_verificados > 0) {
                    mostrarInvitacionOferente();
                }
            }, 5000);
        }, 1000);
        
        function mostrarInvitacionOferente() {
            const invitacion = document.createElement('div');
            invitacion.style.cssText = `
                position: fixed;
                bottom: 20px;
                right: 20px;
                background: rgba(52, 152, 219, 0.9);
                color: white;
                padding: 1rem 1.5rem;
                border-radius: 8px;
                font-size: 0.9em;
                cursor: pointer;
                z-index: 1000;
                transition: all 0.3s ease;
            `;
            invitacion.innerHTML = '¿Quieres registrarte como oferente de servicio?';
            
            invitacion.addEventListener('click', () => {
                window.location.href = 'mapa-nichos.html';
            });
            
            document.body.appendChild(invitacion);
            
            setTimeout(() => {
                invitacion.remove();
            }, 10000);
        }
    }
});

document.addEventListener('contextmenu', e => e.preventDefault());
document.addEventListener('selectstart', e => e.preventDefault());