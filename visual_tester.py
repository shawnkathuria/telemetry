# This script is used for testing the visualisation. It spoofs the radio input by manually sending signals. 
# Add signals to the handler function.

import asyncio
import websockets
import json
import time

async def handler(websocket):
    while True:
        data_final = {"name":"SEN_WSS_FR","value":100}
        await websocket.send(json.dumps(data_final))
        #print(f"Sent")
        await asyncio.sleep(0.001) 
        data_final = {"name":"Beacon","value":50}
        await websocket.send(json.dumps(data_final))
        #print(f"Sent")
        await asyncio.sleep(0.001) 
        data_final = {"name":"Beacon","value":40}
        await websocket.send(json.dumps(data_final))
        #print(f"Sent")
        await asyncio.sleep(0.001) 
        #print("Sending FR")
        data_final = {"name":"SEN_WSS_FR","value":50}
        await websocket.send(json.dumps(data_final))
        #print(f"Sent")
        await asyncio.sleep(0.001) 
        data_final = {"name":"BMS_T_A1","value":1}
        await websocket.send(json.dumps(data_final))
        #print(f"Sent")
        await asyncio.sleep(0.001) 
        data_final = {"name":"SEN_WSS_FR","value":100}
        await websocket.send(json.dumps(data_final))
        #print(f"Sent")
        await asyncio.sleep(0.001) 
        data_final = {"name":"Beacon","value":50}
        await websocket.send(json.dumps(data_final))
        #print(f"Sent")
        await asyncio.sleep(0.001) 
        data_final = {"name":"Beacon","value":40}
        await websocket.send(json.dumps(data_final))
        #print(f"Sent")
        await asyncio.sleep(0.001) 
        #print("Sending FR")
        data_final = {"name":"SEN_WSS_FR","value":50}
        await websocket.send(json.dumps(data_final))
        #print(f"Sent")
        await asyncio.sleep(0.001) 
        data_final = {"name":"BMS_T_A1","value":1}
        await websocket.send(json.dumps(data_final))
        #print(f"Sent")
        await asyncio.sleep(0.001)
        data_final = {"name":"SEN_WSS_FR","value":100}
        await websocket.send(json.dumps(data_final))
        #print(f"Sent")
        await asyncio.sleep(0.001) 
        data_final = {"name":"Beacon","value":50}
        await websocket.send(json.dumps(data_final))
        #print(f"Sent")
        await asyncio.sleep(0.001) 
        data_final = {"name":"Beacon","value":40}
        await websocket.send(json.dumps(data_final))
        #print(f"Sent")
        await asyncio.sleep(0.001) 
        #print("Sending FR")
        data_final = {"name":"SEN_WSS_FR","value":50}
        await websocket.send(json.dumps(data_final))
        #print(f"Sent")
        await asyncio.sleep(0.001) 
        data_final = {"name":"BMS_T_A1","value":1}
        await websocket.send(json.dumps(data_final))
        #print(f"Sent")
        await asyncio.sleep(0.001) 
        data_final = {"name":"SEN_WSS_FR","value":100}
        await websocket.send(json.dumps(data_final))
        #print(f"Sent")
        await asyncio.sleep(0.001) 
        data_final = {"name":"Beacon","value":50}
        await websocket.send(json.dumps(data_final))
        #print(f"Sent")
        await asyncio.sleep(0.001) 
        data_final = {"name":"Beacon","value":40}
        await websocket.send(json.dumps(data_final))
        #print(f"Sent")
        await asyncio.sleep(0.001) 
        #print("Sending FR")
        data_final = {"name":"SEN_WSS_FR","value":50}
        await websocket.send(json.dumps(data_final))
        #print(f"Sent")
        await asyncio.sleep(0.001) 
        data_final = {"name":"BMS_T_A1","value":1}
        await websocket.send(json.dumps(data_final))
        #print(f"Sent")
        await asyncio.sleep(0.001) 
        data_final = {"name":"SEN_WSS_FR","value":100}
        await websocket.send(json.dumps(data_final))
        #print(f"Sent")
        await asyncio.sleep(0.001) 
        data_final = {"name":"Beacon","value":50}
        await websocket.send(json.dumps(data_final))
        #print(f"Sent")
        await asyncio.sleep(0.001) 
        data_final = {"name":"Beacon","value":40}
        await websocket.send(json.dumps(data_final))
        #print(f"Sent")
        await asyncio.sleep(0.001) 
        #print("Sending FR")
        data_final = {"name":"SEN_WSS_FR","value":50}
        await websocket.send(json.dumps(data_final))
        #print(f"Sent")
        await asyncio.sleep(0.001) 
        data_final = {"name":"BMS_T_A1","value":1}
        await websocket.send(json.dumps(data_final))
        #print(f"Sent")
        await asyncio.sleep(0.001) 
        #start_time = time.time()
        data_final = {"name":"SEN_Damper_Pos_FR","value":1}
        print("Sending")
        await websocket.send(json.dumps(data_final))
        #end_time = time.time()
        #elapsed_time = (end_time - start_time)
        #print(elapsed_time)
        await asyncio.sleep(0.001)
        data_final = {"name":"SEN_WSS_FR","value":100}
        await websocket.send(json.dumps(data_final))
        #print(f"Sent")
        await asyncio.sleep(0.001) 
        data_final = {"name":"Beacon","value":50}
        await websocket.send(json.dumps(data_final))
        #print(f"Sent")
        await asyncio.sleep(0.001) 
        data_final = {"name":"Beacon","value":40}
        await websocket.send(json.dumps(data_final))
        #print(f"Sent")
        await asyncio.sleep(0.001) 
        #print("Sending FR")
        data_final = {"name":"SEN_WSS_FR","value":50}
        await websocket.send(json.dumps(data_final))
        #print(f"Sent")
        await asyncio.sleep(0.001) 
        data_final = {"name":"BMS_T_A1","value":1}
        await websocket.send(json.dumps(data_final))
        #print(f"Sent")
        await asyncio.sleep(0.001) 
        data_final = {"name":"SEN_WSS_FR","value":100}
        await websocket.send(json.dumps(data_final))
        #print(f"Sent")
        await asyncio.sleep(0.001) 
        data_final = {"name":"Beacon","value":50}
        await websocket.send(json.dumps(data_final))
        #print(f"Sent")
        await asyncio.sleep(0.001) 
        data_final = {"name":"Beacon","value":40}
        await websocket.send(json.dumps(data_final))
        #print(f"Sent")
        await asyncio.sleep(0.001) 
        #print("Sending FR")
        data_final = {"name":"SEN_WSS_FR","value":50}
        await websocket.send(json.dumps(data_final))
        #print(f"Sent")
        await asyncio.sleep(0.001) 
        data_final = {"name":"BMS_T_A1","value":1}
        await websocket.send(json.dumps(data_final))
        #print(f"Sent")
        await asyncio.sleep(0.001) 
        data_final = {"name":"SEN_WSS_FR","value":100}
        await websocket.send(json.dumps(data_final))
        #print(f"Sent")
        await asyncio.sleep(0.001) 
        data_final = {"name":"Beacon","value":50}
        await websocket.send(json.dumps(data_final))
        #print(f"Sent")
        await asyncio.sleep(0.001) 
        data_final = {"name":"Beacon","value":40}
        await websocket.send(json.dumps(data_final))
        #print(f"Sent")
        await asyncio.sleep(0.001) 
        #print("Sending FR")
        data_final = {"name":"SEN_WSS_FR","value":50}
        await websocket.send(json.dumps(data_final))
        #print(f"Sent")
        await asyncio.sleep(0.001) 
        data_final = {"name":"BMS_T_A1","value":1}
        await websocket.send(json.dumps(data_final))
        #print(f"Sent")
        await asyncio.sleep(0.001) 
        data_final = {"name":"SEN_WSS_FR","value":100}
        await websocket.send(json.dumps(data_final))
        #print(f"Sent")
        await asyncio.sleep(0.001) 
        data_final = {"name":"Beacon","value":50}
        await websocket.send(json.dumps(data_final))
        #print(f"Sent")
        await asyncio.sleep(0.001) 
        data_final = {"name":"Beacon","value":40}
        await websocket.send(json.dumps(data_final))
        #print(f"Sent")
        await asyncio.sleep(0.001) 
        #print("Sending FR")
        data_final = {"name":"SEN_WSS_FR","value":50}
        await websocket.send(json.dumps(data_final))
        #print(f"Sent")
        await asyncio.sleep(0.001) 
        data_final = {"name":"BMS_T_A1","value":1}
        await websocket.send(json.dumps(data_final))
        #print(f"Sent")
        await asyncio.sleep(0.001) 
        data_final = {"name":"SEN_WSS_FR","value":100}
        await websocket.send(json.dumps(data_final))
        #print(f"Sent")
        await asyncio.sleep(0.001) 
        data_final = {"name":"Beacon","value":50}
        await websocket.send(json.dumps(data_final))
        #print(f"Sent")
        await asyncio.sleep(0.001) 
        data_final = {"name":"Beacon","value":40}
        await websocket.send(json.dumps(data_final))
        #print(f"Sent")
        await asyncio.sleep(0.001) 
        #print("Sending FR")
        data_final = {"name":"SEN_WSS_FR","value":50}
        await websocket.send(json.dumps(data_final))
        #print(f"Sent")
        await asyncio.sleep(0.001) 
        data_final = {"name":"BMS_T_A1","value":1}
        await websocket.send(json.dumps(data_final))
        #print(f"Sent")
        await asyncio.sleep(0.001) 
        data_final = {"name":"SEN_WSS_FR","value":100}
        await websocket.send(json.dumps(data_final))
        #print(f"Sent")
        await asyncio.sleep(0.001) 
        data_final = {"name":"Beacon","value":50}
        await websocket.send(json.dumps(data_final))
        #print(f"Sent")
        await asyncio.sleep(0.001) 
        data_final = {"name":"Beacon","value":40}
        await websocket.send(json.dumps(data_final))
        #print(f"Sent")
        await asyncio.sleep(0.001) 
        #print("Sending FR")
        data_final = {"name":"SEN_WSS_FR","value":50}
        await websocket.send(json.dumps(data_final))
        #print(f"Sent")
        await asyncio.sleep(0.001) 
        data_final = {"name":"BMS_T_A1","value":1}
        await websocket.send(json.dumps(data_final))
        #print(f"Sent")
        await asyncio.sleep(0.001) 
        data_final = {"name":"SEN_WSS_FR","value":100}
        await websocket.send(json.dumps(data_final))
        #print(f"Sent")
        await asyncio.sleep(0.001) 
        data_final = {"name":"Beacon","value":50}
        await websocket.send(json.dumps(data_final))
        #print(f"Sent")
        await asyncio.sleep(0.001) 
        data_final = {"name":"Beacon","value":40}
        await websocket.send(json.dumps(data_final))
        #print(f"Sent")
        await asyncio.sleep(0.001) 
        #print("Sending FR")
        data_final = {"name":"SEN_WSS_FR","value":50}
        await websocket.send(json.dumps(data_final))
        #print(f"Sent")
        await asyncio.sleep(0.001) 
        data_final = {"name":"BMS_T_A1","value":1}
        await websocket.send(json.dumps(data_final))
        #print(f"Sent")
        await asyncio.sleep(0.001) 
        data_final = {"name":"SEN_WSS_FR","value":100}
        await websocket.send(json.dumps(data_final))
        #print(f"Sent")
        await asyncio.sleep(0.001) 
        data_final = {"name":"Beacon","value":50}
        await websocket.send(json.dumps(data_final))
        #print(f"Sent")
        await asyncio.sleep(0.001) 
        data_final = {"name":"Beacon","value":40}
        await websocket.send(json.dumps(data_final))
        #print(f"Sent")
        await asyncio.sleep(0.001) 
        #print("Sending FR")
        data_final = {"name":"SEN_WSS_FR","value":50}
        await websocket.send(json.dumps(data_final))
        #print(f"Sent")
        await asyncio.sleep(0.001) 
        data_final = {"name":"BMS_T_A1","value":1}
        await websocket.send(json.dumps(data_final))
        #print(f"Sent")
        await asyncio.sleep(0.001)  

 


# Start the WebSocket server
async def start_server():
    async with websockets.serve(handler, "localhost", 4040):
        print("WebSocket server started...")
        await asyncio.Future()  # Keep the server running

# Run the server
asyncio.run(start_server())
