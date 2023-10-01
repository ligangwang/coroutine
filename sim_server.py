import asyncio
from websockets.server import serve

async def hello(ws):
    async for message in ws:
        print (f'echo: {message}')
        await ws.send(message)

async def run_server():
    async with serve(hello, "localhost", 8765):
        try:
            await asyncio.Future()
        except asyncio.CancelledError:
            print ('canceled')
            return
 
if __name__ == '__main__':
    try:
        asyncio.run(run_server())
    except KeyboardInterrupt:
        print('bye!')
 