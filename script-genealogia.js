// Datos de la genealogía (copiados desde el JSON para acceso directo)
const genealogiaData = {
    "titulo": "Genealogía de Jesucristo según Mateo 1",
    "libro": "Mateo",
    "capitulo": 1,
    "version": "Reina Valera 1960",
    "estructura": {
        "grupos": [
            {
                "nombre": "Primer grupo de 14 generaciones",
                "descripcion": "Desde Abraham hasta David",
                "generaciones": [
                    {
                        "numero": 1,
                        "nombre": "Abraham",
                        "detalle": "Abraham engendró a Isaac",
                        "significado": "Padre de la fe, inicio del pueblo elegido"
                    },
                    {
                        "numero": 2,
                        "nombre": "Isaac",
                        "detalle": "Isaac a Jacob",
                        "significado": "Hijo de la promesa"
                    },
                    {
                        "numero": 3,
                        "nombre": "Jacob",
                        "detalle": "Jacob a Judá y a sus hermanos",
                        "significado": "Padre de las 12 tribus de Israel"
                    },
                    {
                        "numero": 4,
                        "nombre": "Judá",
                        "detalle": "Judá engendró de Tamar a Fares y a Zara",
                        "significado": "Tribu real de la cual vendría el Mesías",
                        "nota_especial": "Menciona a Tamar, nuera de Judá"
                    },
                    {
                        "numero": 5,
                        "nombre": "Fares",
                        "detalle": "Fares a Esrom",
                        "significado": "Hijo gemelo de Tamar"
                    },
                    {
                        "numero": 6,
                        "nombre": "Esrom",
                        "detalle": "Esrom a Aram",
                        "significado": "Continuación de la línea mesiánica"
                    },
                    {
                        "numero": 7,
                        "nombre": "Aram",
                        "detalle": "Aram engendró a Aminadab",
                        "significado": "Parte de la genealogía real"
                    },
                    {
                        "numero": 8,
                        "nombre": "Aminadab",
                        "detalle": "Aminadab a Naasón",
                        "significado": "Padre de Naasón, príncipe de Judá"
                    },
                    {
                        "numero": 9,
                        "nombre": "Naasón",
                        "detalle": "Naasón a Salmón",
                        "significado": "Líder durante el Éxodo"
                    },
                    {
                        "numero": 10,
                        "nombre": "Salmón",
                        "detalle": "Salmón engendró de Rahab a Booz",
                        "significado": "Esposo de Rahab, la prostituta de Jericó",
                        "nota_especial": "Menciona a Rahab, extranjera convertida"
                    },
                    {
                        "numero": 11,
                        "nombre": "Booz",
                        "detalle": "Booz engendró de Rut a Obed",
                        "significado": "Esposo de Rut, ejemplo de redentor",
                        "nota_especial": "Menciona a Rut, mujer moabita"
                    },
                    {
                        "numero": 12,
                        "nombre": "Obed",
                        "detalle": "Obed a Isaí",
                        "significado": "Padre de Isaí, abuelo de David"
                    },
                    {
                        "numero": 13,
                        "nombre": "Isaí",
                        "detalle": "Isaí engendró al rey David",
                        "significado": "Padre del rey David"
                    },
                    {
                        "numero": 14,
                        "nombre": "David",
                        "detalle": "El rey David",
                        "significado": "Rey de Israel, punto culminante del primer grupo"
                    }
                ]
            },
            {
                "nombre": "Segundo grupo de 14 generaciones",
                "descripcion": "Desde David hasta la deportación a Babilonia",
                "generaciones": [
                    {
                        "numero": 15,
                        "nombre": "Salomón",
                        "detalle": "El rey David engendró a Salomón de la que fue mujer de Urías",
                        "significado": "Hijo de David y Betsabé",
                        "nota_especial": "Menciona a la mujer de Urías (Betsabé)"
                    },
                    {
                        "numero": 16,
                        "nombre": "Roboam",
                        "detalle": "Salomón engendró a Roboam",
                        "significado": "Rey que dividió el reino"
                    },
                    {
                        "numero": 17,
                        "nombre": "Abías",
                        "detalle": "Roboam a Abías",
                        "significado": "Rey de Judá"
                    },
                    {
                        "numero": 18,
                        "nombre": "Asa",
                        "detalle": "Abías a Asa",
                        "significado": "Rey reformador de Judá"
                    },
                    {
                        "numero": 19,
                        "nombre": "Josafat",
                        "detalle": "Asa engendró a Josafat",
                        "significado": "Rey aliado con Israel"
                    },
                    {
                        "numero": 20,
                        "nombre": "Joram",
                        "detalle": "Josafat a Joram",
                        "significado": "Rey de Judá"
                    },
                    {
                        "numero": 21,
                        "nombre": "Uzías",
                        "detalle": "Joram a Uzías",
                        "significado": "Rey próspero de Judá"
                    },
                    {
                        "numero": 22,
                        "nombre": "Jotam",
                        "detalle": "Uzías engendró a Jotam",
                        "significado": "Rey justo de Judá"
                    },
                    {
                        "numero": 23,
                        "nombre": "Acaz",
                        "detalle": "Jotam a Acaz",
                        "significado": "Rey idólatra de Judá"
                    },
                    {
                        "numero": 24,
                        "nombre": "Ezequías",
                        "detalle": "Acaz a Ezequías",
                        "significado": "Rey reformador, prolongó su vida"
                    },
                    {
                        "numero": 25,
                        "nombre": "Manasés",
                        "detalle": "Ezequías engendró a Manasés",
                        "significado": "Rey más malvado de Judá"
                    },
                    {
                        "numero": 26,
                        "nombre": "Amón",
                        "detalle": "Manasés a Amón",
                        "significado": "Rey idólatra de Judá"
                    },
                    {
                        "numero": 27,
                        "nombre": "Josías",
                        "detalle": "Amón a Josías",
                        "significado": "Rey reformador, último buen rey"
                    },
                    {
                        "numero": 28,
                        "nombre": "Jeconías",
                        "detalle": "Josías engendró a Jeconías y a sus hermanos, en el tiempo de la deportación a Babilonia",
                        "significado": "Rey durante el exilio",
                        "nota_especial": "Marca el fin del reino de Judá"
                    }
                ]
            },
            {
                "nombre": "Tercer grupo de 14 generaciones",
                "descripcion": "Desde la deportación a Babilonia hasta Cristo",
                "generaciones": [
                    {
                        "numero": 29,
                        "nombre": "Salatiel",
                        "detalle": "Después de la deportación a Babilonia, Jeconías engendró a Salatiel",
                        "significado": "Líder post-exilio"
                    },
                    {
                        "numero": 30,
                        "nombre": "Zorobabel",
                        "detalle": "Salatiel a Zorobabel",
                        "significado": "Gobernador de Judá, reconstruyó el templo"
                    },
                    {
                        "numero": 31,
                        "nombre": "Abiud",
                        "detalle": "Zorobabel engendró a Abiud",
                        "significado": "Continuación de la línea mesiánica"
                    },
                    {
                        "numero": 32,
                        "nombre": "Eliaquim",
                        "detalle": "Abiud a Eliaquim",
                        "significado": "Parte de la genealogía"
                    },
                    {
                        "numero": 33,
                        "nombre": "Azor",
                        "detalle": "Eliaquim a Azor",
                        "significado": "Parte de la genealogía"
                    },
                    {
                        "numero": 34,
                        "nombre": "Sadoc",
                        "detalle": "Azor engendró a Sadoc",
                        "significado": "Parte de la genealogía"
                    },
                    {
                        "numero": 35,
                        "nombre": "Aquim",
                        "detalle": "Sadoc a Aquim",
                        "significado": "Parte de la genealogía"
                    },
                    {
                        "numero": 36,
                        "nombre": "Eliud",
                        "detalle": "Aquim a Eliud",
                        "significado": "Parte de la genealogía"
                    },
                    {
                        "numero": 37,
                        "nombre": "Eleazar",
                        "detalle": "Eliud engendró a Eleazar",
                        "significado": "Parte de la genealogía"
                    },
                    {
                        "numero": 38,
                        "nombre": "Matán",
                        "detalle": "Eleazar a Matán",
                        "significado": "Parte de la genealogía"
                    },
                    {
                        "numero": 39,
                        "nombre": "Jacob",
                        "detalle": "Matán a Jacob",
                        "significado": "Parte de la genealogía"
                    },
                    {
                        "numero": 40,
                        "nombre": "José",
                        "detalle": "Jacob engendró a José, marido de María",
                        "significado": "Esposo de María, carpintero de Nazaret"
                    },
                    {
                        "numero": 41,
                        "nombre": "María",
                        "detalle": "María, de la cual nació Jesús",
                        "significado": "Madre de Jesús, virgen",
                        "nota_especial": "El nacimiento virginal"
                    },
                    {
                        "numero": 42,
                        "nombre": "Jesús",
                        "detalle": "Jesús, llamado el Cristo",
                        "significado": "El Mesías prometido, Salvador del mundo"
                    }
                ]
            }
        ]
    },
    "nacimiento_jesus": {
        "descripcion": "El nacimiento de Jesucristo fue así",
        "detalles": [
            "Estando desposada María su madre con José",
            "Antes que se juntasen, se halló que había concebido del Espíritu Santo",
            "José su marido, como era justo, no quería infamarla",
            "Quiso dejarla secretamente",
            "Un ángel del Señor se apareció en sueños a José",
            "Le dijo: 'José, hijo de David, no temas recibir a María tu mujer'",
            "Porque lo que en ella es engendrado, del Espíritu Santo es",
            "Y dará a luz un hijo, y llamarás su nombre JESÚS",
            "Porque él salvará a su pueblo de sus pecados",
            "Se cumplió la profecía: 'He aquí, una virgen concebirá y dará a luz un hijo'",
            "Y llamarás su nombre Emanuel, que traducido es: Dios con nosotros"
        ]
    },
    "mujeres_mencionadas": [
        {
            "nombre": "Tamar",
            "descripcion": "Nuera de Judá, cananea",
            "significado": "Ejemplo de fe y determinación en la línea mesiánica"
        },
        {
            "nombre": "Rahab",
            "descripcion": "Prostituta de Jericó, cananea",
            "significado": "Extranjera convertida, muestra la gracia de Dios"
        },
        {
            "nombre": "Rut",
            "descripcion": "Mujer moabita, viuda",
            "significado": "Extranjera incluida en el plan de salvación"
        },
        {
            "nombre": "Betsabé",
            "descripcion": "Mujer de Urías, esposa de David",
            "significado": "Ejemplo del perdón y la misericordia divina"
        },
        {
            "nombre": "María",
            "descripcion": "Virgen, madre de Jesús",
            "significado": "Elegida para el milagro del nacimiento virginal"
        }
    ]
};

// Estado de la aplicación
let currentSection = 'genealogia';

// Inicialización cuando se carga el DOM
document.addEventListener('DOMContentLoaded', function() {
    inicializarAplicacion();
});

// Función principal de inicialización
function inicializarAplicacion() {
    cargarGenealogia();
    cargarMujeres();
    cargarNacimiento();
    configurarNavegacion();
    configurarModal();
    animarEntrada();
}

// Cargar la genealogía en los tres grupos
function cargarGenealogia() {
    genealogiaData.estructura.grupos.forEach((grupo, grupoIndex) => {
        const grupoId = `grupo${grupoIndex + 1}`;
        const container = document.getElementById(grupoId);

        grupo.generaciones.forEach((generacion, index) => {
            const generacionElement = crearElementoGeneracion(generacion, grupoIndex + 1);
            container.appendChild(generacionElement);

            // Animación secuencial
            setTimeout(() => {
                generacionElement.style.opacity = '1';
                generacionElement.style.transform = 'translateY(0)';
            }, index * 100);
        });
    });
}

// Crear elemento HTML para cada generación
function crearElementoGeneracion(generacion, grupoNumero) {
    const div = document.createElement('div');
    div.className = `generacion-item ${generacion.nota_especial ? 'especial' : ''}`;
    div.setAttribute('data-nombre', generacion.nombre);
    div.onclick = () => mostrarModal(generacion, grupoNumero);

    div.innerHTML = `
        <div class="generacion-numero">${generacion.numero}</div>
        <div class="generacion-nombre">${generacion.nombre}</div>
        <div class="generacion-detalle">${generacion.detalle}</div>
    `;

    return div;
}

// Cargar las mujeres mencionadas
function cargarMujeres() {
    const container = document.querySelector('.mujeres-container');

    genealogiaData.mujeres_mencionadas.forEach((mujer, index) => {
        const mujerCard = document.createElement('div');
        mujerCard.className = 'mujer-card';

        mujerCard.innerHTML = `
            <div class="mujer-nombre">${mujer.nombre}</div>
            <div class="mujer-descripcion">${mujer.descripcion}</div>
            <div class="mujer-significado">${mujer.significado}</div>
        `;

        // Animación de entrada
        setTimeout(() => {
            mujerCard.style.opacity = '1';
            mujerCard.style.transform = 'translateY(0)';
        }, index * 200);

        container.appendChild(mujerCard);
    });
}

// Cargar información del nacimiento
function cargarNacimiento() {
    const container = document.querySelector('.nacimiento-detalles');

    genealogiaData.nacimiento_jesus.detalles.forEach((detalle, index) => {
        const detalleElement = document.createElement('p');
        detalleElement.textContent = detalle;

        // Animación secuencial
        setTimeout(() => {
            detalleElement.style.opacity = '1';
            detalleElement.style.transform = 'translateX(0)';
        }, index * 300);

        container.appendChild(detalleElement);
    });
}

// Configurar navegación entre secciones
function configurarNavegacion() {
    const navButtons = document.querySelectorAll('.nav-btn');

    navButtons.forEach(button => {
        button.addEventListener('click', function() {
            const sectionId = this.getAttribute('data-section');

            // Remover clase active de todos los botones
            navButtons.forEach(btn => btn.classList.remove('active'));

            // Agregar clase active al botón clicado
            this.classList.add('active');

            // Cambiar sección visible
            cambiarSeccion(sectionId);
        });
    });
}

// Cambiar entre secciones
function cambiarSeccion(sectionId) {
    // Ocultar todas las secciones
    const sections = document.querySelectorAll('.section');
    sections.forEach(section => {
        section.classList.remove('active');
    });

    // Mostrar la sección seleccionada
    const targetSection = document.getElementById(sectionId);
    if (targetSection) {
        targetSection.classList.add('active');
        currentSection = sectionId;
    }
}

// Configurar modal de información detallada
function configurarModal() {
    const modal = document.getElementById('infoModal');
    const closeBtn = document.querySelector('.close');

    // Cerrar modal al hacer clic en la X
    closeBtn.onclick = function() {
        modal.style.display = 'none';
    };

    // Cerrar modal al hacer clic fuera del contenido
    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = 'none';
        }
    };

    // Cerrar modal con tecla Escape
    document.addEventListener('keydown', function(event) {
        if (event.key === 'Escape' && modal.style.display === 'block') {
            modal.style.display = 'none';
        }
    });
}

// Mostrar modal con información detallada
function mostrarModal(generacion, grupoNumero) {
    const modal = document.getElementById('infoModal');

    // Llenar el modal con información
    document.getElementById('modalNombre').textContent = generacion.nombre;
    document.getElementById('modalNumero').textContent = `Generación #${generacion.numero}`;
    document.getElementById('modalGrupo').textContent = `Grupo ${grupoNumero}`;
    document.getElementById('modalDetalle').textContent = generacion.detalle;
    document.getElementById('modalSignificado').textContent = generacion.significado;

    // Mostrar nota especial si existe
    const notaEspecialElement = document.getElementById('modalNotaEspecial');
    if (generacion.nota_especial) {
        notaEspecialElement.innerHTML = `<strong>Nota especial:</strong> ${generacion.nota_especial}`;
        notaEspecialElement.style.display = 'block';
    } else {
        notaEspecialElement.style.display = 'none';
    }

    // Mostrar modal con animación
    modal.style.display = 'block';
    setTimeout(() => {
        modal.querySelector('.modal-content').style.transform = 'translateY(0)';
        modal.querySelector('.modal-content').style.opacity = '1';
    }, 10);
}

// Animaciones de entrada
function animarEntrada() {
    // Animar elementos de la primera sección visible
    const elementosAnimar = document.querySelectorAll('.generacion-item, .grupo-genealogico');

    elementosAnimar.forEach((elemento, index) => {
        elemento.style.opacity = '0';
        elemento.style.transform = 'translateY(20px)';

        setTimeout(() => {
            elemento.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
            elemento.style.opacity = '1';
            elemento.style.transform = 'translateY(0)';
        }, index * 50);
    });
}

// Funcionalidad adicional para mejorar la experiencia
document.addEventListener('DOMContentLoaded', function() {
    // Agregar efecto de brillo a personas especiales
    setInterval(() => {
        const jesusElement = document.querySelector('[data-nombre="Jesús"]');
        if (jesusElement) {
            jesusElement.style.transform = 'scale(1.02)';
            setTimeout(() => {
                jesusElement.style.transform = 'scale(1)';
            }, 1000);
        }
    }, 3000);

    // Agregar tooltips a elementos especiales
    const elementosEspeciales = document.querySelectorAll('.generacion-item.especial');
    elementosEspeciales.forEach(elemento => {
        elemento.title = 'Haz clic para ver más información';
    });

    // Smooth scroll para navegación
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
});

// Función para buscar personas en la genealogía
function buscarPersona(nombre) {
    const todasLasGeneraciones = [];
    genealogiaData.estructura.grupos.forEach(grupo => {
        todasLasGeneraciones.push(...grupo.generaciones);
    });

    return todasLasGeneraciones.find(generacion =>
        generacion.nombre.toLowerCase().includes(nombre.toLowerCase())
    );
}

// Función para resaltar conexiones familiares
function resaltarConexion(persona1, persona2) {
    const elemento1 = document.querySelector(`[data-nombre="${persona1}"]`);
    const elemento2 = document.querySelector(`[data-nombre="${persona2}"]`);

    if (elemento1) elemento1.classList.add('resaltado');
    if (elemento2) elemento2.classList.add('resaltado');

    setTimeout(() => {
        if (elemento1) elemento1.classList.remove('resaltado');
        if (elemento2) elemento2.classList.remove('resaltado');
    }, 3000);
}

// Función para mostrar estadísticas de la genealogía
function mostrarEstadisticas() {
    const totalGeneraciones = 42;
    const grupos = 3;
    const mujeresMencionadas = 5;
    const generacionesEspeciales = document.querySelectorAll('.generacion-item.especial').length;

    console.log('Estadísticas de la Genealogía:');
    console.log(`- Total de generaciones: ${totalGeneraciones}`);
    console.log(`- Número de grupos: ${grupos}`);
    console.log(`- Mujeres mencionadas: ${mujeresMencionadas}`);
    console.log(`- Generaciones especiales: ${generacionesEspeciales}`);
}

// Ejecutar estadísticas al cargar
document.addEventListener('DOMContentLoaded', mostrarEstadisticas);