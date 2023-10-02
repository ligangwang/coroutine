import asyncio
from websockets.server import serve
import websockets
from concurrent.futures import ProcessPoolExecutor
from service import on_msg_recv

connected = set()
executor = ProcessPoolExecutor()
loop = asyncio.get_event_loop()

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

async def receive_from_market(msg):
    global executor
    await loop.run_in_executor(executor, on_msg_recv, msg)

async def server_main():
    async with serve(connect, "localhost", 8764):
        try:
            await asyncio.Future()
        except asyncio.CancelledError:
            print ('canceled')
            return

async def market_main():
    async for ws in websockets.connect('ws://localhost:8765'):
        try:
            async for msg in ws:
                await receive_from_market(msg)
        except ConnectionRefusedError:# (ConnectionAbortedError, ConnectionRefusedError,ConnectionResetError, ConnectionError):
            continue
        except:
            print('catch call')

async def main():
    try:
        await asyncio.gather(
            server_main(),
            market_main()
        )
    except ConnectionRefusedError:
        print('market connection failed')

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, ConnectionRefusedError):
        print('bye!')
