// Connect to the Python mock server directly on 127.0.0.1:4040
const PYTHON_WS_HOST = '127.0.0.1';
const PYTHON_WS_PORT = 4040;
const socket = new WebSocket(`ws://${PYTHON_WS_HOST}:${PYTHON_WS_PORT}`);

/**
 * Key: is a {string}, datapoint name (e.g., "temperature", "humidity", "pressure")
 * Value: {Object} containing:
 *    - {Chart} chart - The Chart.js instance where the datapoint is plotted.
 *    - {Object} dataset - The specific dataset object inside the chart corresponding to the datapoint.
*/
charts = new Map();
Chart.defaults.font.size = 8;

// Creation of graphs
createGraph(["SEN_WSS_FL", "SEN_WSS_FR", "SEN_WSS_RL", "SEN_WSS_RR"]);
createGraph(["LV_BPT_Front", "LV_BPT_Rear"]);
createGraph(["SEN_Damper_Pos_FL", "SEN_Damper_Pos_FR", "SEN_Damper_Pos_RL", "SEN_Damper_Pos_RR"]);
createGraph(["INV_Motor_Speed"]);
createGraph(["SEN_G_FORCE_X", "SEN_G_FORCE_Y", "SEN_G_FORCE_Z"]);
createGraph(["INV_Commanded_Torque", "INV_Torque_Feedback", "VCU_INV_Torque_Command"]);

function createGraph(dataPoints) { 
    const canvas_el = document.createElement("canvas");
    canvas_el.id = 'chart-' + dataPoints.join('-');
    const wrapper_el = document.createElement("div");
    wrapper_el.classList.add("graph-wrapper");
    wrapper_el.appendChild(canvas_el);
    document.getElementById("charts").appendChild(wrapper_el);

    let datasets = dataPoints.map(name => ({
        label: name,
        data: [],
        borderWidth: 1
    }));

    let chart = new Chart(canvas_el, {
        type: 'line',
        data: { labels: [], datasets: datasets },
        options: {
            scales: {
                x: {
                    type: 'time',
                    time: { unit: 'second', tooltipFormat: 'HH:mm:ss' },
                    title: { display: true, text: 'Time' }
                },
                y: { beginAtZero: true }
            },
            animation: { duration: 0 },
            responsive: true,
            maintainAspectRatio: false
        }
    });

    for (let dataset of chart.data.datasets) {
        charts.set(dataset.label, { chart: chart, dataset: dataset });
    }
}

function triggerFault(fault) {
    document.getElementById("errorMessage").innerText = "Error: " + fault;
    document.getElementById("errorPopup").style.display = "block";
}

function closePopup() {
    document.getElementById("errorPopup").style.display = "none";
}

function updateTable(name, value){
    document.getElementById(name).innerText = value;
}

let dataBuffer = [];
const UPDATE_INTERVAL_MS = 100;

// Periodically flush dataBuffer to charts
setInterval(() => {
    if (dataBuffer.length === 0) return;
    let groupedData = {};
    dataBuffer.forEach(({ name, value, time }) => {
        if (!groupedData[name]) groupedData[name] = [];
        groupedData[name].push({ x: time, y: value });
    });

    Object.keys(groupedData).forEach(name => {
        if (!charts.has(name)) return;
        const chart = charts.get(name).chart;
        const dataset = charts.get(name).dataset.data;
        while (dataset.length + groupedData[name].length > 60) dataset.shift();
        dataset.push(...groupedData[name]);
        chart.update();
    });

    dataBuffer = [];
}, UPDATE_INTERVAL_MS);

// --- WebSocket event handling ---
socket.onopen = () => {
    console.log(`Connected to Python WebSocket server at ws://${PYTHON_WS_HOST}:${PYTHON_WS_PORT}`);
};

socket.onmessage = (msg) => {
    const dataObject = JSON.parse(msg.data);
    const now = new Date();

    // Fault handling
    if ((dataObject.value === 1 && dataObject.name.startsWith("LV_Fault_")) ||
        (dataObject.name === "INV_DC_Bus_Current" && dataObject.value > 350) ||
        (dataObject.name === "INV_DC_Bus_Voltage" && dataObject.value > 303)) {
        triggerFault(dataObject.name);
        return;
    } else if (dataObject.name === "LV_FILTERED_V" || dataObject.name === "BeaconCount" || 
               dataObject.name.startsWith("BMS") || dataObject.name.startsWith("SEN_TT") || 
               dataObject.name === "LV_Vehicle_State") {
        updateTable(dataObject.name, dataObject.value);
        return;
    }

    // Adjust BPT sensors
    if (dataObject.name === "LV_BPT_Front") {
        dataObject.value = ((dataObject.value / 4095 * 3.3 * 4 + 0.05) - 0.5) * 25;
    } else if (dataObject.name === "LV_BPT_Rear") {
        dataObject.value = ((dataObject.value / 4095 * 3.3 * 4 + 0.043) - 0.5) * 25;
    }

    dataBuffer.push({ name: dataObject.name, value: dataObject.value, time: now });
};

socket.onclose = () => {
    console.warn('Disconnected from Python WebSocket server');
};

socket.onerror = (e) => {
    console.error('WebSocket error:', e);
};

// Optional: error popup helper
function showErrorPopup(errorMessage, duration = 5000) {
    let popupContainer = document.getElementById('error-popup-container');
    const popup = document.createElement('div');
    popup.className = 'error-popup';
    popup.textContent = errorMessage;
    popupContainer.appendChild(popup);
    setTimeout(() => {
        popup.classList.add('fade-out');
        setTimeout(() => popup.remove(), 500);
    }, duration);
}
