// Acceso Iniciático - Solo para quienes han cruzado el umbral
(function() {
    'use strict';
    
    // Verificar si el visitante ha completado el ritual
    function verificarIniciacion() {
        const umbralCruzado = localStorage.getItem('cora_umbral_cruzado');
        const presencias = localStorage.getItem('cora_presencias_silenciosas');
        
        return umbralCruzado && presencias;
    }
    
    // Activar navegación oculta para iniciados
    function activarNavegacionOculta() {
        if (!verificarIniciacion()) return;
        
        // Escuchar combinación de teclas: p + r + e + s (presencias)
        let secuencia = '';
        let timeout;
        
        document.addEventListener('keydown', function(e) {
            clearTimeout(timeout);
            secuencia += e.key.toLowerCase();
            
            if (secuencia.includes('pres')) {
                window.location.href = 'presencias.html';
                return;
            }
            
            // Limpiar secuencia después de 2 segundos
            timeout = setTimeout(() => {
                secuencia = '';
            }, 2000);
            
            // Mantener solo últimos 4 caracteres
            if (secuencia.length > 4) {
                secuencia = secuencia.slice(-4);
            }
        });
        
        // Activar también con triple clic en el punto (si existe)
        const punto = document.getElementById('punto');
        if (punto) {
            let clics = 0;
            punto.addEventListener('click', function() {
                clics++;
                if (clics === 3) {
                    setTimeout(() => {
                        window.location.href = 'presencias.html';
                    }, 500);
                }
                
                setTimeout(() => {
                    clics = 0;
                }, 1000);
            });
        }
    }
    
    // Activar solo si la página está cargada
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', activarNavegacionOculta);
    } else {
        activarNavegacionOculta();
    }
})();