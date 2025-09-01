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

function activarSecuencia(textoIntencion) {
    if (secuenciaIniciada) return;
    secuenciaIniciada = true;
    
    localStorage.setItem('cora_umbral_cruzado', JSON.stringify({
        timestamp: new Date().toISOString(),
        intencion: textoIntencion,
        dominio: 'CO-RA.ecosistema.mx',
        ritual_completado: true
    }));
    
    document.body.classList.add('vibrar');
    
    setTimeout(() => {
        document.body.classList.remove('vibrar');
        punto.classList.add('destello-momento');
        
        setTimeout(() => {
            punto.classList.remove('destello-momento');
            punto.style.opacity = '1';
            
            setTimeout(() => {
                cuestionamiento.style.opacity = '1';
            }, 2000);
        }, 800);
    }, 400);
}

punto.addEventListener('click', function() {
    if (secuenciaIniciada) {
        punto.style.transform = 'translate(-50%, -50%) scale(0)';
        setTimeout(() => {
            cuestionamiento.innerHTML = 'Ahora sabes.';
        }, 1000);
    }
});

document.addEventListener('contextmenu', e => e.preventDefault());
document.addEventListener('selectstart', e => e.preventDefault());