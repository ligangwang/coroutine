import asyncio
from websockets.server import serve
import websockets

connected = set()

count = 0
async def connect(ws):
    global connected, count
    try:
        connected.add(ws)
        print('client connected')
        while True:
            await ws.send(f'count: {count}')
            count += 1
            await asyncio.sleep(1)
    except websockets.exceptions.ConnectionClosedOK:
        print('client connection closed.')
    finally:
        connected.remove(ws)
        print('client disconnected')

async def main():
    async with serve(connect, "localhost", 8765):
        try:
            await asyncio.Future()
        except asyncio.CancelledError:
            print ('canceled')
            return
 
if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('bye!')
 