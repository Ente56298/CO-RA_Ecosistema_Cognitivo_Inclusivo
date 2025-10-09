const startButton = document.getElementById('startButton');
const buttonText = document.getElementById('buttonText');
const resetButton = document.getElementById('resetButton');
const speedRange = document.getElementById('speedRange');
const lineageContainer = document.getElementById('lineageContainer');
const progressBar = document.getElementById('progressBar');

// Accesibilidad CO•RA
let highContrast = false;
let textSize = 100;
let reduceMotion = false;

const contrastBtn = document.getElementById('contrastBtn');
const textSizeBtn = document.getElementById('textSizeBtn');
const motionBtn = document.getElementById('motionBtn');

contrastBtn?.addEventListener('click', () => {
    highContrast = !highContrast;
    document.body.classList.toggle('high-contrast', highContrast);
});

textSizeBtn?.addEventListener('click', () => {
    textSize = textSize >= 150 ? 100 : textSize + 10;
    document.body.style.fontSize = `${textSize}%`;
});

motionBtn?.addEventListener('click', () => {
    reduceMotion = !reduceMotion;
    document.body.classList.toggle('reduce-motion', reduceMotion);
});

// Atajos de teclado
document.addEventListener('keydown', (e) => {
    if (e.key === 'c' || e.key === 'C') {
        contrastBtn?.click();
    } else if (e.key === '+' || e.key === '=') {
        textSizeBtn?.click();
    } else if (e.key === 'Escape') {
        motionBtn?.click();
    } else if (e.key === ' ' && e.target === document.body) {
        e.preventDefault();
        startButton?.click();
    }
});

const characterDetails = {
    "Adán": `Progenitor de la humanidad.<br><strong>Esposa:</strong> Eva<br><strong>Años de vida:</strong> 930 años<br><strong>Edad (al nacer Set):</strong> 130 años<br><br><strong>Hazaña Notable:</strong> Nombrar a todos los seres vivientes.<br><em>Referencias: Génesis 2:19-20, Génesis 5:3-5</em>`,
    "Set": `Continuador del linaje piadoso.<br><strong>Años de vida:</strong> 912 años<br><strong>Edad (al nacer Enós):</strong> 105 años<br><br><strong>Hazaña Notable:</strong> Su nacimiento representó la esperanza tras la muerte de Abel.<br><em>Referencias: Génesis 4:25, Génesis 5:6-8</em>`,
    "Henoc": `Bisabuelo de Noé, conocido por su fe.<br><strong>Años de vida:</strong> 365 años<br><br><strong>Hazaña Notable:</strong> Fue llevado al cielo por Dios sin experimentar la muerte.<br><em>Referencias: Génesis 5:24, Hebreos 11:5</em>`,
    "Noé": `Patriarca que sobrevivió al Diluvio.<br><strong>Esposa:</strong> No se nombra<br><strong>Años de vida:</strong> 950 años<br><strong>Edad (al nacer sus hijos):</strong> 500 años<br><br><strong>Hazaña Notable:</strong> Construir el arca para salvar a su familia y a los animales.<br><em>Referencias: Génesis 6:9, Génesis 9:29</em>`,
    "Sem": `Hijo de Noé y antepasado de Abraham.<br><strong>Años de vida:</strong> 600 años<br><strong>Edad (al nacer Arfaxad):</strong> 100 años<br><br><strong>Hazaña Notable:</strong> Recibió la bendición principal de su padre.<br><em>Referencias: Génesis 9:26, Génesis 11:10-11</em>`,
    "Cam": `Hijo de Noé y progenitor de naciones como Egipto, Etiopía y Canaán.<br><br><strong>Hazaña Notable:</strong> Su descendencia dio origen a grandes civilizaciones del mundo antiguo.<br><em>Referencia: Génesis 10:6</em>`,
    "Jafet": `Hijo de Noé, padre de los pueblos de Europa y Asia Menor.<br><br><strong>Hazaña Notable:</strong> Ser el ancestro de las naciones que se dispersaron por las costas.<br><em>Referencia: Génesis 10:5</em>`,
    "Nimrod": `El primer rey poderoso y un gran cazador.<br><br><strong>Hazaña Notable:</strong> Fundó el primer gran imperio después del diluvio, incluyendo Babel y Nínive.<br><em>Referencia: Génesis 10:8-10</em>`,
    "Éber": `Ancestro de Abraham y figura clave en el linaje de Sem.<br><br><strong>Hazaña Notable:</strong> Es considerado el antepasado epónimo del pueblo 'hebreo'.<br><em>Referencia: Génesis 10:21</em>`,
    "Péleg": `Su nombre significa 'división'.<br><br><strong>Hazaña Notable:</strong> Su vida coincidió con la dispersión de la humanidad tras la Torre de Babel.<br><em>Referencia: Génesis 10:25</em>`,
    "Abram": `Conocido como Abraham, el 'Padre de la Fe'.<br><strong>Esposas:</strong> Sara, Agar, Queturá<br><strong>Años de vida:</strong> 175 años<br><br><strong>Hazaña Notable:</strong> Obedecer a Dios al dejar su tierra (Ur) para ir a Canaán, estableciendo el pacto divino.<br><em>Referencias: Génesis 12:1-3, Génesis 25:7</em>`,
    "Ismael": `Primer hijo de Abraham.<br><br><strong>Hazaña Notable:</strong> Convertirse en el progenitor de doce príncipes y una gran nación, los pueblos árabes.<br><em>Referencia: Génesis 21:17-18</em>`,
    "Isaac": `Hijo de la promesa.<br><strong>Esposa:</strong> Rebeca<br><strong>Años de vida:</strong> 180 años<br><strong>Edad (al nacer sus hijos):</strong> 60 años<br><br><strong>Hazaña Notable:</strong> Heredero del pacto y padre de Jacob y Esaú.<br><em>Referencias: Génesis 26:3-4, Génesis 35:28</em>`,
    "Israel": `Originalmente llamado Jacob.<br><strong>Esposas:</strong> Lea, Raquel, Bilha, Zilpa<br><strong>Años de vida:</strong> 147 años<br><br><strong>Hazaña Notable:</strong> Luchar con un ángel y recibir el nombre de Israel. Padre de los 12 fundadores de las tribus de Israel.<br><em>Referencias: Génesis 32:28, Génesis 47:28</em>`,
    "Esaú": `Hijo mayor de Isaac, también conocido como Edom.<br><strong>Esposas:</strong> Judit, Basemat, Mahalat<br><br><strong>Hazaña Notable:</strong> Reconciliarse con su hermano Jacob. Progenitor del pueblo edomita.<br><em>Referencias: Génesis 33:4, Génesis 36:1-2</em>`
};

const lineageData = [
    { parent: "Adán", children: ["Set"] },
    { parent: "Set", children: ["Enós"] },
    { parent: "Enós", children: ["Cainán"] },
    { parent: "Cainán", children: ["Mahalalel"] },
    { parent: "Mahalalel", children: ["Jéred"] },
    { parent: "Jéred", children: ["Henoc"] },
    { parent: "Henoc", children: ["Matusalén"] },
    { parent: "Matusalén", children: ["Lámec"] },
    { parent: "Lámec", children: ["Noé"] },
    { parent: "Noé", children: ["Sem", "Cam", "Jafet"], note: "Los hijos de Noé" },
    { parent: "Jafet", children: ["Gómer", "Magog", "Madai", "Javán", "Tubal", "Mésec", "Tirás"] },
    { parent: "Gómer", children: ["Asquenaz", "Rifat", "Togarmá"] },
    { parent: "Javán", children: ["Elisá", "Tarsis", "Quitim", "Rodanim"] },
    { parent: "Cam", children: ["Cus", "Misraim", "Fut", "Canaán"] },
    { parent: "Cus", children: ["Sebá", "Havilá", "Sabtá", "Raamá", "Sabtecá", "Nimrod"], note: "Nimrod, el primer poderoso" },
    { parent: "Raamá", children: ["Sebá", "Dedán"] },
    { parent: "Misraim", children: ["Ludeos", "Anameos", "Lehabitas", "Naftuhítas", "Patruseos", "Casluhítas", "Caftoritas"], note: "De Casluhítas descienden los filisteos" },
    { parent: "Canaán", children: ["Sidón", "Het", "Jebuseos", "Amorreos", "Gergeseos", "Heveos", "Araceos", "Sineos", "Arvadeos", "Semareos", "Hamateos"] },
    { parent: "Sem", children: ["Elam", "Asur", "Arfaxad", "Lud", "Aram"] },
    { parent: "Aram", children: ["Us", "Hul", "Guéter", "Mas"] },
    { parent: "Arfaxad", children: ["Sélah"] },
    { parent: "Sélah", children: ["Éber"] },
    { parent: "Éber", children: ["Péleg", "Joctán"] },
    { parent: "Joctán", children: ["Almodad", "Sélef", "Hasar-mávet", "Jérah", "Hadoram", "Uzal", "Diclá", "Obal", "Abimael", "Sebá", "Ofir", "Havilá", "Jobab"] },
    { parent: "Péleg", children: ["Reú"], note: "Linaje de Sem hacia Abraham" },
    { parent: "Reú", children: ["Serug"] },
    { parent: "Serug", children: ["Nahor"] },
    { parent: "Nahor", children: ["Térah"] },
    { map: { url: "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e8/Fertile_Crescent_map.png/1280px-Fertile_Crescent_map.png", caption: "Mapa del Creciente Fértil, la región donde se desarrollaron estas narrativas." }, note: "El Viaje de los Patriarcas" },
    { parent: "Térah", children: ["Abram (Abraham)"] },
    { parent: "Abraham", children: ["Isaac", "Ismael"], note: "Hijos de Abraham" },
    { parent: "Ismael", children: ["Nebaiot", "Quedar", "Adbeel", "Mibsam", "Mismá", "Dumá", "Masá", "Hadad", "Temá", "Jetur", "Nafís", "Quedmá"] },
    { parent: "Abraham", children: ["Zimrán", "Jocsán", "Medán", "Madián", "Isbac", "Súah"], note: "Hijos con Queturá" },
    { parent: "Jocsán", children: ["Sebá", "Dedán"] },
    { parent: "Madián", children: ["Efá", "Éfer", "Hanoc", "Abidá", "Eldaá"] },
    { parent: "Isaac", children: ["Esaú", "Israel (Jacob)"] },
    { parent: "Esaú", children: ["Elifaz", "Reuel", "Jeús", "Jaalam", "Coré"], note: "Descendientes de Esaú (Edom)" },
    { parent: "Elifaz", children: ["Temán", "Omar", "Sefó", "Gatam", "Quenaz", "Amalec"] },
    { parent: "Reuel", children: ["Náhat", "Zérah", "Samá", "Mizá"] }
];

let currentIndex = 0;
let animationInterval;
let isPaused = false;
let animationSpeed = 1000;

function setupExpandableNode(clickableElement, containerElement, detailsText) {
    clickableElement.classList.add('cursor-pointer', 'relative', 'pr-8');
    clickableElement.setAttribute('tabindex', '0');
    clickableElement.setAttribute('role', 'button');
    clickableElement.setAttribute('aria-expanded', 'false');
    
    const icon = document.createElement('span');
    icon.className = 'expand-icon';
    icon.textContent = '+';
    icon.setAttribute('aria-hidden', 'true');
    clickableElement.appendChild(icon);
    
    const detailsBox = document.createElement('div');
    detailsBox.className = 'details-box';
    detailsBox.innerHTML = `<p class="text-gray-300 text-sm leading-relaxed">${detailsText}</p>`;
    detailsBox.setAttribute('role', 'region');
    containerElement.appendChild(detailsBox);
    
    const toggleDetails = (e) => {
        e.stopPropagation();
        const isExpanded = detailsBox.classList.toggle('expanded');
        icon.textContent = isExpanded ? '−' : '+';
        clickableElement.setAttribute('aria-expanded', isExpanded.toString());
    };
    
    clickableElement.addEventListener('click', toggleDetails);
    clickableElement.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
            e.preventDefault();
            toggleDetails(e);
        }
    });
}

function updateSpeed() {
    animationSpeed = 2200 - speedRange.value;
    if (animationInterval && !isPaused) {
        clearInterval(animationInterval);
        animationInterval = setInterval(animateStep, animationSpeed);
    }
}

speedRange.addEventListener('input', updateSpeed);

function animateStep() {
    if (currentIndex >= lineageData.length) {
        clearInterval(animationInterval);
        buttonText.textContent = "Finalizado";
        startButton.disabled = true;
        return;
    }
    const step = lineageData[currentIndex];
    createGenerationView(step.parent, step.children, step.note, step.map);
    const progress = ((currentIndex + 1) / lineageData.length) * 100;
    progressBar.style.width = `${progress}%`;
    progressBar.parentElement?.setAttribute('aria-valuenow', Math.round(progress).toString());
    currentIndex++;
}

function createGenerationView(parentName, childrenNames, note, mapData) {
    const generationWrapper = document.createElement('div');
    generationWrapper.className = 'w-full max-w-5xl flex flex-col items-center p-4 bg-gray-800/50 rounded-lg shadow-md mb-8 node';
    
    if (note) {
        const noteEl = document.createElement('h3');
        noteEl.className = 'text-lg font-semibold text-blue-300 mb-4 text-center';
        noteEl.textContent = note;
        generationWrapper.appendChild(noteEl);
    }

    if (mapData) {
        const mapContainer = document.createElement('figure');
        mapContainer.className = 'map-container';
        const mapImg = document.createElement('img');
        mapImg.src = mapData.url;
        mapImg.alt = 'Mapa del Creciente Fértil';
        const mapCaption = document.createElement('figcaption');
        mapCaption.innerHTML = mapData.caption;
        mapContainer.appendChild(mapImg);
        mapContainer.appendChild(mapCaption);
        generationWrapper.appendChild(mapContainer);
    }

    if (parentName) {
        const parentWrapper = document.createElement('div');
        parentWrapper.className = 'flex flex-col items-center w-auto';
        const parentNode = document.createElement('div');
        parentNode.className = 'bg-gray-700 text-white py-2 px-5 rounded-lg shadow-lg border-2 parent-node';
        parentNode.textContent = parentName;
        parentWrapper.appendChild(parentNode);
        generationWrapper.appendChild(parentWrapper);
        const detailsKey = parentName.split(' ')[0].replace('(', '');
        const details = characterDetails[detailsKey];
        if (details) {
            setupExpandableNode(parentNode, parentWrapper, details);
        }
    }
    
    if (childrenNames && childrenNames.length > 0) {
        if(parentName) {
            const lineDown = document.createElement('div');
            lineDown.className = 'line-down';
            generationWrapper.appendChild(lineDown);
        }
        const childrenContainer = document.createElement('div');
        childrenContainer.className = 'children-container w-full';
        const lineContainer = document.createElement('div');
        lineContainer.className = 'line-container';
        const lineAcross = document.createElement('div');
        lineAcross.className = 'line-across';
        const childrenFlex = document.createElement('div');
        childrenFlex.className = 'flex flex-wrap justify-center gap-x-4 gap-y-6 relative';
        
        childrenNames.forEach((childName) => {
            const childWrapper = document.createElement('div');
            childWrapper.className = 'relative flex flex-col items-center';
            const childLineUp = document.createElement('div');
            childLineUp.className = 'child-line-up';
            const childNode = document.createElement('div');
            childNode.className = 'bg-gray-700 text-white py-2 px-4 rounded-lg shadow-lg border-2 child-node z-10';
            childNode.textContent = childName;
            if(parentName) {
                childWrapper.appendChild(childLineUp);
            }
            childWrapper.appendChild(childNode);
            const detailsKey = childName.split(' ')[0].replace('(', '');
            const details = characterDetails[detailsKey];
            if(details){
                setupExpandableNode(childNode, childWrapper, details);
            }
            childrenFlex.appendChild(childWrapper);
        });
        
        lineContainer.appendChild(lineAcross);
        childrenContainer.appendChild(lineContainer);
        childrenContainer.appendChild(childrenFlex);
        generationWrapper.appendChild(childrenContainer);
    }
    
    lineageContainer.appendChild(generationWrapper);
    void generationWrapper.offsetWidth; 
    generationWrapper.classList.add('visible');
    
    setTimeout(() => {
        const childrenFlex = generationWrapper.querySelector('.flex');
        if (childrenFlex && childrenFlex.children.length > 1) {
            const firstChild = childrenFlex.firstElementChild;
            const lastChild = childrenFlex.lastElementChild;
            const lineAcross = generationWrapper.querySelector('.line-across');
            const start = firstChild.offsetLeft + firstChild.offsetWidth / 2;
            const end = lastChild.offsetLeft + lastChild.offsetWidth / 2;
            lineAcross.style.left = `${start}px`;
            lineAcross.style.width = `${end - start}px`;
        } else if (childrenFlex && childrenFlex.children.length === 1) {
            const lineAcross = generationWrapper.querySelector('.line-across');
            if(lineAcross) lineAcross.style.display = 'none';
        }
    }, 10);
    
    generationWrapper.scrollIntoView({ behavior: 'smooth', block: 'center' });
}

function togglePause() {
    isPaused = !isPaused;
    if (isPaused) {
        clearInterval(animationInterval);
        startButton.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16"><path d="m11.596 8.697-6.363 3.692c-.54.313-1.233-.066-1.233-.697V4.308c0-.63.692-1.01 1.233-.696l6.363 3.692a.802.802 0 0 1 0 1.393z"/></svg><span>Continuar</span>`;
    } else {
        animationInterval = setInterval(animateStep, animationSpeed);
        startButton.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16"><path d="M5.5 3.5A1.5 1.5 0 0 1 7 5v6a1.5 1.5 0 0 1-3 0V5A1.5 1.5 0 0 1 5.5 3.5zm5 0A1.5 1.5 0 0 1 12 5v6a1.5 1.5 0 0 1-3 0V5A1.5 1.5 0 0 1 10.5 3.5z"/></svg><span>Pausar</span>`;
    }
}

startButton.addEventListener('click', () => {
    if (animationInterval) {
        togglePause();
    } else {
        if(currentIndex === 0) animateStep();
        animationInterval = setInterval(animateStep, animationSpeed);
        startButton.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16"><path d="M5.5 3.5A1.5 1.5 0 0 1 7 5v6a1.5 1.5 0 0 1-3 0V5A1.5 1.5 0 0 1 5.5 3.5zm5 0A1.5 1.5 0 0 1 12 5v6a1.5 1.5 0 0 1-3 0V5A1.5 1.5 0 0 1 10.5 3.5z"/></svg><span>Pausar</span>`;
    }
});

resetButton.addEventListener('click', () => {
    clearInterval(animationInterval);
    animationInterval = null;
    currentIndex = 0;
    isPaused = false;
    lineageContainer.innerHTML = '';
    progressBar.style.width = '0%';
    startButton.disabled = false;
    startButton.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16"><path d="m11.596 8.697-6.363 3.692c-.54.313-1.233-.066-1.233-.697V4.308c0-.63.692-1.01 1.233-.696l6.363 3.692a.802.802 0 0 1 0 1.393z"/></svg><span>Iniciar Animación</span>`;
});

updateSpeed();
