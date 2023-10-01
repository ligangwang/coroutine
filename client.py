import asyncio
import datetime

import asyncio
from websockets.sync.client import connect
import websockets

async def main():
    async with websockets.connect("ws://localhost:8764") as ws:
        async for msg in ws:
            print(msg)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('bye!')
