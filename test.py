import asyncio
import websockets


async def hello():
    uri = "ws://127.0.0.1:8000/ws/chat_room/2?session_key=ehlxj116ee55ta289slckh8xkfpi11ga"
    async with websockets.connect(uri) as websocket:
        await websocket.send('{"message": "Hello world!", "username": "asdaaaa"}')
        res = await websocket.recv()
        print(res)


asyncio.get_event_loop().run_until_complete(hello())