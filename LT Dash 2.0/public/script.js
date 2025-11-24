// Connect to the Python mock server directly on 127.0.0.1:4040
const PYTHON_WS_HOST = '127.0.0.1';
const PYTHON_WS_PORT = 4040;
const socket = new WebSocket(`ws://${PYTHON_WS_HOST}:${PYTHON_WS_PORT}`);

socket.onopen = () => {
    console.log(`Connected to Python WebSocket server at ws://${PYTHON_WS_HOST}:${PYTHON_WS_PORT}`);
};

socket.onmessage = (msg) => {
    const dataObject = JSON.parse(msg.data);
    const now = new Date();

    // Handle faults
    if ((dataObject.value == 1 && dataObject.name.startsWith("LV_Fault_")) || 
        (dataObject.name == "INV_DC_Bus_Current" && dataObject.value > 350) || 
        (dataObject.name == "INV_DC_Bus_Voltage" && dataObject.value > 303)) {
        triggerFault(dataObject.name);
        return;
    } else if(dataObject.name == "LV_FILTERED_V" || dataObject.name == "BeaconCount" || 
        dataObject.name.startsWith("BMS") || dataObject.name.startsWith("SEN_TT") || 
        dataObject.name == "LV_Vehicle_State") {
        updateTable(dataObject.name, dataObject.value);
        return;
    }

    // Adjust BPT sensor values
    if (dataObject.name == "LV_BPT_Front") {
        dataObject.value = ((dataObject.value / 4095 * 3.3 * 4 + 0.05) - 0.5) * 25;
    } else if (dataObject.name == "LV_BPT_Rear") {
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
