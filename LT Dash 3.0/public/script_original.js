const url = new URL(window.location.href);
const serverIp = url.hostname;
const socket = new WebSocket(`ws://${serverIp}:4040`);

/**
 * Key: is a {string}, datapoint name (e.g., "temperature", "humidity", "pressure")
 * Value: {Object} containing:
 *    - {Chart} chart - The Chart.js instance where the datapoint is plotted.
 *    - {Object} dataset - The specific dataset object inside the chart corresponding to the datapoint.
*/
charts = new Map();
Chart.defaults.font.size = 8;


// Creation of graphs. Order here is what determines the order of the graphs on the page. Top to bottom, left to right.
// HTML currently set up to display 3 graphs per row, 2 rows per screen height.
createGraph(["SEN_WSS_FL", "SEN_WSS_FR", "SEN_WSS_RL", "SEN_WSS_RR"]);
createGraph(["LV_BPT_Front", "LV_BPT_Rear"]);
createGraph(["SEN_Damper_Pos_FL", "SEN_Damper_Pos_FR", "SEN_Damper_Pos_RL", "SEN_Damper_Pos_RR"]);
createGraph(["INV_Motor_Speed"]);
createGraph(["SEN_G_FORCE_X", "SEN_G_FORCE_Y", "SEN_G_FORCE_Z"]);
createGraph(["INV_Commanded_Torque", "INV_Torque_Feedback", "VCU_INV_Torque_Command"]);

/**
 * Creates a single line chart displaying multiple datasets, one for each provided datapoint name.
 * 
 * @param {string[]} dataPoints - A single datapoint name or an array of datapoint names to be displayed as separate lines on the same chart.
 * @return {Chart} The created chart.
 *
 * The chart is stored in `charts` map.
 */
function createGraph(dataPoints) { 
    const canvas_el = document.createElement("canvas");
    canvas_el.id = 'chart-' + dataPoints.join('-'); //Order doesn't matter, since this is never referenced directly.
    const wrapper_el = document.createElement("div");
    wrapper_el.classList.add("graph-wrapper");
    wrapper_el.appendChild(canvas_el);
    document.getElementById("charts").appendChild(wrapper_el);

    // for each datapoint name, create a dataset object and add it to the datasets array
    let datasets = dataPoints.map(name => ({
        label: name,
        data: [],
        borderWidth: 1
    }));

    let chart = new Chart(canvas_el, {
        type: 'line',
        data: {
            labels: [],
            datasets: datasets
        },
        options: {
            scales: {
                x: {
                    type: 'time',
                    time: {
                        unit: 'second',
                        tooltipFormat: 'HH:mm:ss'
                    },
                    title: {
                        display: true,
                        text: 'Time'
                    }
                },
                y: {
                    beginAtZero: true
                }
            },
            animation: {
                duration: 0
            },
            responsive: true,
            maintainAspectRatio: false,
        }
    });

    for (let dataset of chart.data.datasets) {
        charts.set(dataset.label, {
            chart: chart,
            dataset: dataset
        });
    }
}

// function addFault(fault) {
//     const faultList = document.getElementById('faultcode-list');
//     const faultItem = document.createElement('li');
//     faultItem.textContent = fault;
//     if(!faultList.children.length) {
//         faultList.appendChild(faultItem); 
//     }
//     faultList.insertBefore(faultItem, faultList.firstChild);
// }

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

setInterval(() => {
    if (dataBuffer.length === 0) return;
    let groupedData = {};
    // Group data points by name
    dataBuffer.forEach(({ name, value, time }) => {
        if (!groupedData[name]) {
            groupedData[name] = [];
        }
        groupedData[name].push({ x: time, y: value });
    });

    // Update charts
    Object.keys(groupedData).forEach(name => {
        if (!charts.has(name)) return;
        const chart = charts.get(name).chart;
        const dataset = charts.get(name).dataset.data;

        // Remove old points if exceeding limit
        while (dataset.length + groupedData[name].length > 60) {
            dataset.shift();
        }

        dataset.push(...groupedData[name]);
        chart.update();
    });

    // Clear buffer after processing
    dataBuffer = [];
}, UPDATE_INTERVAL_MS);






last_time = 0;
socket.onmessage = (msg) => {
    curr_time = Date.now();
    console.log(curr_time - last_time);
    last_time = curr_time;
    dataObject = JSON.parse(msg.data); //expected format: {"name": "datapoint_name", "value": (float)}
    console.log(dataObject);
    let now = new Date();
    // Fault Handling:
    // For simplicity, we can just prefix faults with something, like "FAULT_".
    if((dataObject.value == 1 && dataObject.name.startsWith("LV_Fault_")) || 
        (dataObject.name == "INV_DC_Bus_Current" && dataObject.value > 350) 
        || (dataObject.name == "INV_DC_Bus_Voltage" && dataObject.value > 303) ) {
        triggerFault(dataObject.name); // remove "FAULT_" prefix
        return;
    }
    else if(dataObject.name == "LV_FILTERED_V" || dataObject.name == "BeaconCount" || 
        dataObject.name.startsWith("BMS") || dataObject.name.startsWith("SEN_TT") || dataObject.name == "LV_Vehicle_State") {
        updateTable(dataObject.name, dataObject.value);
        return;
    }
    //Data Handling:
    //if(charts.get(dataObject.name) == undefined) return;

    // const chart = charts.get(dataObject.name).chart;
    // const dataset = charts.get(dataObject.name).dataset.data;
    // if (dataset.length > 60) {
    //     dataset.shift();
    // }
    // dataset.push({ x: now, y: dataObject.value });
    // chart.update();
    if(dataObject.name == "LV_BPT_Front"){
       dataObject.value = ((dataObject.value/4095*3.3*4+0.05)-0.5)*25
    }
    else if (dataObject.name == "LV_BPT_Rear"){
       dataObject.value = ((dataObject.value/4095*3.3*4+0.043)-0.5)*25
    }

    dataBuffer.push({ name: dataObject.name, value: dataObject.value, time: new Date() });
}


socket.onopen = () => {
    // dataDisplay.textContent = 'Connected to server. Awaiting data...';
};

socket.onclose = () => {
    alert('Disconnected from server');
};

socket.onerror = (e) => {
    console.error("WebSocket Error:", e);
}

//Creates an error popup for client, default duration of 5s.
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