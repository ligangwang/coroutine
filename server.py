import asyncio
import socket
import websockets

async def run_server(host='127.0.0.1', port=55555):
    sock = socket.socket()
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, port))
    sock.listen()
    while True:
        client_sock, addr = await sock.accept()
        print('Connection from', addr)
        await handle_client(client_sock)


async def handle_client(sock):
    while True:
        received_data = await sock.recv(4096)
        if not received_data:
            break
        await sock.sendall(received_data)

    print('Client disconnected:', sock.getpeername())
    sock.close()



if __name__ == '__main__':
    asyncio.run(run_server())
