document.addEventListener("DOMContentLoaded", function () {
    const zonaSelect = document.getElementById("zona");
    const regionSelect = document.getElementById("region");
    const comunaSelect = document.getElementById("comuna");
    const regionContainer = document.getElementById("region-container");
    const comunaContainer = document.getElementById("comuna-container");

    const regionesComunas = {
        "Zona 1 (Arica y Parinacota - Antofagasta)": {
            "Región de Arica y Parinacota": [
                "Arica",
                "Camarones",
                "Putre",
                "General Lagos"
            ],
            "Región de Antofagasta": [
                "Antofagasta",
                "Mejillones",
                "Sierra Gorda",
                "Taltal",
                "Calama"
            ]
        },
        "Zona 2 (Atacama - Coquimbo)": {
            "Región de Atacama": [
                "Copiapo",
                "Caldera",
                "Vallenar",
                "Chañaral",
                "Diego de Almagro",
                "Freirina",
                "Tierra Amarilla"
            ],
            "Región de Coquimbo": [
                "La Serena",
                "Coquimbo",
                "Ovalle",
                "Illapel",
                "Vicuña",
                "Salamanca"
            ]
        },
        "Zona 3 (Valparaiso - Maule)": {
            "Región de Valparaiso": [
                "Valparaiso",
                "Viña del Mar",
                "Quilpue",
                "Villa Alemana",
                "San Antonio",
                "Los Andes",
                "San Felipe",
                "Quillota",
                "La Ligua",
                "Petorcas"
            ],
            "Región de Maule": [
                "Talca",
                "Curico",
                "Linares",
                "Constitucion",
                "Parral",
                "Cauquenes",
                "Molina",
                "San Javier"
            ]
        },
        "Zona 4 (BIOBIO - Los Lagos)": {
            "Región del BIOBIO": [
                "Concepcion",
                "Talcahuano",
                "Coronel",
                "Los Angeles",
                "Chillan",
                "Chillan Viejo",
                "Lota",
                "Tome",
                "Penco",
                "Cabrero"
            ],
            "Región de Los Lagos": [
                "Puerto Montt",
                "Puerto Varas",
                "Osorno",
                "Castro",
                "Ancud",
                "Frutillar"
            ]
        },
        "Zona 5 (Aysen - Magallanes)": {
            "Región de Aysen del general Carlos  Ibáñez del campo": [
                "Coyhaique",
                "Puerto Aysen",
                "Chile Chico",
                "Cochrane",
                "Cisnes",
                "O'higgins",
                "Guaitecas"
            ],
            "Región de Magallanes y de la antartica Chilena": [
                "Puerto Arenas",
                "Puerto Natales",
                "Porvenir",
                "Puerto Williams",
                "Cabo de Hornos",
                "Torres del Paine"
            ]
        }
    };

    function populateSelect(select, options) {
        select.innerHTML = "";
        options.forEach(option => {
            const optionElement = document.createElement("option");
            optionElement.text = option;
            select.add(optionElement);
        });
    }

    function updateRegiones(zona) {
        regionSelect.disabled = false;
        regionContainer.style.display = "block";
        const regiones = Object.keys(regionesComunas[zona]);
        populateSelect(regionSelect, regiones);
        comunaSelect.innerHTML = "<option value=''>Seleccione una comuna</option>";
        comunaSelect.disabled = true;
        comunaContainer.style.display = "none";
    }

    function updateComunas(region) {
        comunaSelect.disabled = false;
        comunaContainer.style.display = "block";
        const comunas = regionesComunas[zonaSelect.value][region];
        populateSelect(comunaSelect, comunas);
    }

    zonaSelect.addEventListener("change", function () {
        const selectedZona = zonaSelect.value;
        updateRegiones(selectedZona);
    });

    regionSelect.addEventListener("change", function () {
        const selectedRegion = regionSelect.value;
        updateComunas(selectedRegion);
    });

    regionSelect.disabled = true;
    regionContainer.style.display = "none";
    comunaSelect.disabled = true;
    comunaContainer.style.display = "none";

    populateSelect(zonaSelect, Object.keys(regionesComunas));

    zonaSelect.disabled = true;
});