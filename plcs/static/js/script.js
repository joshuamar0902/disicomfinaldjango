// --- Conexión WebSocket con el servidor de Django Channels ---
const plcSocket = new WebSocket('ws://' + window.location.host + '/ws/chat/');

// --- Función reutilizable para actualizar un medidor (velocímetro) ---
function updateGauge(gaugeId, value, maxValue) {
    const gauge = document.getElementById(gaugeId);
    if (!gauge) return; // Si el medidor no existe, no hagas nada

    const needle = gauge.querySelector('.needle');
    const scoreValue = gauge.querySelector('.score-value');

    // Mapeo de valor a ángulo de la aguja (-135° a 135°, un arco de 270°)
    const percentage = Math.min(Math.max(value, 0), maxValue) / maxValue;
    const angle = -135 + (percentage * 270);

    // Aplicar la rotación a la aguja y actualizar el texto
    needle.style.transform = `translateX(-50%) rotate(${angle}deg)`;
    
    // Formatear el texto para que tenga un aspecto consistente
    if (Number.isInteger(value)) {
        scoreValue.textContent = value.toString().padStart(4, '0');
    } else {
        scoreValue.textContent = value.toFixed(2);
    }
}

// --- Función para actualizar el medidor booleano ---
function updateBooleanToggle(bitValue) {
    const button = document.getElementById('boolean-toggle-btn');
    const text = document.getElementById('boolean-toggle-text');
    if (!button || !text) return;

    if (bitValue) { // Si el bit es TRUE
        text.textContent = 'ON';
        button.classList.add('status-on');
        button.classList.remove('status-off');
    } else { // Si el bit es FALSE
        text.textContent = 'OFF';
        button.classList.add('status-off');
        button.classList.remove('status-on');
    }
}

// --- Función para controlar la visibilidad de la alerta ---
function updateAlert(bitValue) {
    const alertCard = document.getElementById('alert-card');
    if (!alertCard) return;

    // La lógica es: mostrar la alerta cuando el bit está APAGADO (false)
    if (bitValue === false) {
        alertCard.style.display = 'block';
    } else {
        alertCard.style.display = 'none';
    }
}


// --- Evento principal: Se dispara cada vez que llega un mensaje del servidor ---
plcSocket.onmessage = function(e) {
    const parsedData = JSON.parse(e.data);
    
    // Asegúrate que el tipo de mensaje es el correcto
    if (parsedData.type === 'plc_data_update' || parsedData.type === 'plc_update') {
        const values = parsedData.data;

        // 1. Actualizar el Medidor Booleano y la Alerta
        updateBooleanToggle(values.Bit_1);
        updateAlert(values.Bit_1);

        // 2. Actualizar los Velocímetros con sus respectivos valores
        //    (Ajusta los valores máximos según las especificaciones de tu PLC)
        updateGauge('gauge1', values.Valor_int, 1000);   // Max de 1000 para el entero
        updateGauge('gauge2', values.Valor_float, 100);  // Max de 500 para el flotante
        updateGauge('gauge3', values.Contador, 500);    // Max de 2000 para el contador
        updateGauge('gauge4', values.Valor_Demo, 100);
    }
};

// --- Manejadores de eventos de la conexión WebSocket ---
plcSocket.onopen = function(e) {
    console.log('✅ Conexión WebSocket establecida con éxito.');
};

plcSocket.onclose = function(e) {
    console.error('❌ Socket cerrado. Intentando reconectar...');
    // Aquí podrías agregar lógica para intentar reconectar después de unos segundos
};
// --- ANIMACIÓN DE LLENADO Y VACIADO DEL CILINDRO ---
let nivel = 0;
let subiendo = true;
const contenido = document.getElementById("contenidocilindro");

function animarCilindro() {
  if (subiendo) {
    nivel += 2; // velocidad de subida
    if (nivel >= 100) {
      nivel = 100;
      subiendo = false;
    }
  } else {
    nivel -= 2; // velocidad de bajada
    if (nivel <= 0) {
      nivel = 0;
      subiendo = true;
    }
  }

  contenido.style.height = `${nivel}%`;
}

// ejecuta la animación cada 100ms
setInterval(animarCilindro, 100);
