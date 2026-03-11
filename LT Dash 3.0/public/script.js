// Connect to the Python mock server directly on 127.0.0.1:4040
// const PYTHON_WS_HOST = '0.0.0.0';
// const PYTHON_WS_PORT = 4040;
// const socket = new WebSocket(`ws://${PYTHON_WS_HOST}:${PYTHON_WS_PORT}`);
const wsProto = (window.location.protocol === "https:") ? "wss" : "ws";
const wsHost = window.location.hostname;   // hostname WITHOUT port
const wsPort = 4040;
const socket = new WebSocket(`${wsProto}://${wsHost}:${wsPort}`);


/**
 * For each tab we maintain a Map:
 *   key: signal name
 *   value: { chart, dataset }
 */
const TAB_IDS = ["tab1", "tab2", "tab3"];
const tabCharts = {
    tab1: new Map(),
    tab2: new Map(),
    tab3: new Map(),
};

Chart.defaults.font.size = 8;

// Shared graph configuration (same on all tabs for now)
const GRAPH_GROUPS = [
    ["SEN_WSS_FL", "SEN_WSS_FR", "SEN_WSS_RL", "SEN_WSS_RR"],
    ["LV_BPT_Front", "LV_BPT_Rear"],
    ["SEN_Damper_Pos_FL", "SEN_Damper_Pos_FR", "SEN_Damper_Pos_RL", "SEN_Damper_Pos_RR"],
    ["INV_Motor_Speed"],
    ["SEN_G_FORCE_X", "SEN_G_FORCE_Y", "SEN_G_FORCE_Z"],
    ["INV_Commanded_Torque", "INV_Torque_Feedback", "VCU_INV_Torque_Command"],
];

function createGraph(dataPoints, containerId, chartMap) { 
    const container = document.getElementById(containerId);
    if (!container) return;

    const canvas_el = document.createElement("canvas");
    canvas_el.id = 'chart-' + dataPoints.join('-') + '-' + containerId;
    const wrapper_el = document.createElement("div");
    wrapper_el.classList.add("graph-wrapper");
    wrapper_el.appendChild(canvas_el);
    container.appendChild(wrapper_el);

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
        chartMap.set(dataset.label, { chart: chart, dataset: dataset });
    }
}

// Initialize graphs for each tab
window.addEventListener("DOMContentLoaded", () => {
    TAB_IDS.forEach(tabId => {
        const containerId = `charts-${tabId}`;
        const chartMap = tabCharts[tabId];
        GRAPH_GROUPS.forEach(group => createGraph(group, containerId, chartMap));
    });

    // Tab switching behavior
    const buttons = document.querySelectorAll(".tab-button");
    const tabContents = document.querySelectorAll(".tab-content");

    buttons.forEach(btn => {
        btn.addEventListener("click", () => {
            const targetTab = btn.getAttribute("data-tab");

            buttons.forEach(b => b.classList.toggle("active", b === btn));
            tabContents.forEach(tc => {
                tc.classList.toggle("active", tc.getAttribute("data-tab") === targetTab);
            });
        });
    });
});

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

    // Push updates into every tab's charts so that, for now,
    // all tabs show the same information.
    Object.keys(groupedData).forEach(name => {
        TAB_IDS.forEach(tabId => {
            const chartMap = tabCharts[tabId];
            if (!chartMap.has(name)) return;
            const chart = chartMap.get(name).chart;
            const dataset = chartMap.get(name).dataset.data;
            while (dataset.length + groupedData[name].length > 60) dataset.shift();
            dataset.push(...groupedData[name]);
            chart.update();
        });
    });

    dataBuffer = [];
}, UPDATE_INTERVAL_MS);

// --- WebSocket event handling ---
socket.onopen = () => {
    // console.log(`Connected to Python WebSocket server at ws://${PYTHON_WS_HOST}:${PYTHON_WS_PORT}`);
};

// socket.onmessage = (msg) => {
//     const dataObject = JSON.parse(msg.data);
//     const now = new Date();

//     // Fault handling
//     if ((dataObject.value === 1 && dataObject.name.startsWith("LV_Fault_")) ||
//         (dataObject.name === "INV_DC_Bus_Current" && dataObject.value > 350) ||
//         (dataObject.name === "INV_DC_Bus_Voltage" && dataObject.value > 303)) {
//         triggerFault(dataObject.name);
//         return;
//     } else if (dataObject.name === "LV_FILTERED_V" || dataObject.name === "BeaconCount" || 
//                dataObject.name.startsWith("BMS") || dataObject.name.startsWith("SEN_TT") || 
//                dataObject.name === "LV_Vehicle_State") {
//         updateTable(dataObject.name, dataObject.value);
//         return;
//     }

//     // Adjust BPT sensors
//     if (dataObject.name === "LV_BPT_Front") {
//         dataObject.value = ((dataObject.value / 4095 * 3.3 * 4 + 0.05) - 0.5) * 25;
//     } else if (dataObject.name === "LV_BPT_Rear") {
//         dataObject.value = ((dataObject.value / 4095 * 3.3 * 4 + 0.043) - 0.5) * 25;
//     }

//     dataBuffer.push({ name: dataObject.name, value: dataObject.value, time: now });
// };

socket.onmessage = (msg) => {
    const payload = JSON.parse(msg.data);
    // console.log("ws payload keys:", Object.keys(payload).slice(0, 5));
    const now = new Date();

    // payload is { signalName: value, ... }
    for (const [name, valueRaw] of Object.entries(payload)) {
        let value = valueRaw;

        // Fault handling (same logic, but per-signal)
        if ((value === 1 && name.startsWith("LV_Fault_")) ||
            (name === "INV_DC_Bus_Current" && value > 350) ||
            (name === "INV_DC_Bus_Voltage" && value > 303)) {
            triggerFault(name);
            continue;
        } else if (name === "LV_FILTERED_V" || name === "BeaconCount" ||
                   name.startsWith("BMS") || name.startsWith("SEN_TT") ||
                   name === "LV_Vehicle_State") {
            updateTable(name, value);
            continue;
        }

        // Adjust BPT sensors
        if (name === "LV_BPT_Front") {
            value = ((value / 4095 * 3.3 * 4 + 0.05) - 0.5) * 25;
        } else if (name === "LV_BPT_Rear") {
            value = ((value / 4095 * 3.3 * 4 + 0.043) - 0.5) * 25;
        }

        dataBuffer.push({ name, value, time: now });
    }
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
