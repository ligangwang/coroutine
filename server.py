import asyncio
from websockets.server import serve
import websockets
from concurrent.futures import ProcessPoolExecutor
from service import on_msg_recv
from datastore import init_db

connected = set()
executor = ProcessPoolExecutor()

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
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(executor, on_msg_recv, msg)

async def server_main():
    async with serve(connect, "localhost", 8764):
        try:
            await asyncio.Future()
        except asyncio.CancelledError:
            print ('canceled')
            return

reconnect_interval = 1

async def market_main():
    global reconnect_interval
    print('connecting to market...')
    try:    
        async with websockets.connect('ws://localhost:8765') as ws:
            async for msg in ws:
                await receive_from_market(msg)
    except asyncio.CancelledError:
        print('market connection canceled')
    except ConnectionRefusedError:# (ConnectionAbortedError, ConnectionRefusedError,ConnectionResetError, ConnectionError):
        print(f"connection refused, retrying in {reconnect_interval} second(s)...")
        await asyncio.sleep(reconnect_interval)
        if reconnect_interval < 30:
            reconnect_interval *= 2
        await market_main()

async def main():
    await asyncio.gather(
        server_main(),
        market_main()
    )

if __name__ == '__main__':
    try:
        init_db()    
        asyncio.run(main())
    except KeyboardInterrupt:
        print('bye!')
