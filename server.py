import asyncio
from websockets.server import serve
import websockets

connected = set()


async def connect(ws):
    global connected
    try:
        connected.add(ws)
        print('connected')
        async for msg in ws:
            print(msg)
            await ws.send(msg)
    except websockets.exceptions.ConnectionClosedOK:
        print('connection closed.')
    finally:
        connected.remove(ws)
        print('disconnected')

async def send_to_clients(msg):
    global connected
    for ws in connected:
        await ws.send(msg)
    print(f'broadcasting to {len(connected)} clients: {msg}')
    # websockets.broadcast(connected, f'relayed: {msg}')

async def server_main():
    async with serve(connect, "localhost", 8764):
        try:

            await asyncio.Future()
        except asyncio.CancelledError:
            print ('canceled')
            return

async def client_main():
    async with websockets.connect('ws://localhost:8765') as ws:
        async for msg in ws:
            await send_to_clients(msg)

async def main():
    await asyncio.gather(
        server_main(),
        client_main()
    )

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('bye!')
