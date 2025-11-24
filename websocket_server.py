# websocket_server.py
import asyncio
import websockets
import json
from functools import partial

async def handler(websocket, path, CONNECTIONS):
    CONNECTIONS.add(websocket)
    print(f"[WS] Client connected ({len(CONNECTIONS)} total)")
    try:
        await websocket.wait_closed()
    finally:
        CONNECTIONS.remove(websocket)
        print(f"[WS] Client disconnected ({len(CONNECTIONS)} total)")

async def serve(CONNECTIONS, signals, host="127.0.0.1", port=4040):
    """
    Start WebSocket server and broadcast signals continuously.
    """
    # Use functools.partial to pass CONNECTIONS to handler without breaking signature
    bound_handler = partial(handler, CONNECTIONS=CONNECTIONS)
    server = await websockets.serve(bound_handler, host, port)

    async def broadcast_loop():
        while True:
            if CONNECTIONS and signals:
                payload = {name: sig.value for name, sig in signals.items()}
                dead = set()
                for ws in CONNECTIONS:
                    try:
                        await ws.send(json.dumps(payload))
                    except:
                        dead.add(ws)
                CONNECTIONS.difference_update(dead)
            await asyncio.sleep(0.1)

    asyncio.create_task(broadcast_loop())
    print(f"[WS] WebSocket server started on ws://{host}:{port}")
    return server
