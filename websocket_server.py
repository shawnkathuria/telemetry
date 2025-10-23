import websockets

async def echo_handler(CONNECTIONS, websocket):
    CONNECTIONS.add(websocket)
    try:
        await websocket.wait_closed()
    finally:
        CONNECTIONS.remove(websocket)

async def serve(CONNECTIONS):
    # TODO does this work for passing in arguments to a funciton that is an argument?
    websockets.serve(echo_handler(CONNECTIONS), "localhost", 4040)