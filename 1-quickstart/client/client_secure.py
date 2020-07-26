#!/usr/bin/env python

# WSS (WS over TLS) client example, with a self-signed certificate

import asyncio
import pathlib
import ssl
import websockets

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
cert = pathlib.Path(__file__).parent.parent/"server"/"ssl"/"mycert.pem"
ssl_context.load_verify_locations(cert)
ssl_context.check_hostname = False


async def hello():
    uri = "wss://localhost:8765/hello"
    async with websockets.connect(uri, ssl=ssl_context) as websocket:
        name = input("What's your name? ")
        await websocket.send(name)
        print(f'> {name}')

        greeting = await websocket.recv()
        print(f'< {greeting}')

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(hello())
