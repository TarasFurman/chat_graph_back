import asyncio
import websockets

async def hello():
    uri = "ws://127.0.0.1:8000/ws?session_key=asd"
    async with websockets.connect(uri) as websocket:
        await websocket.send({'messgae': "Hello world!"})
        await websocket.recv()

asyncio.get_event_loop().run_until_complete(hello())
