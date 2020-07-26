#!/usr/bin/env python

# WSS (WS over TLS) server example, with a self-signed certificate

import asyncio
import pathlib
import ssl
import websockets


async def hello(websocket, path):
    print(f"Received request in path {path}")
    if path == "/hello":
        name = await websocket.recv()
        print(f'< {name}')

        greeting = f"Hello {name}!"

        await websocket.send(greeting)
        print(f"> {greeting}")
    else:
        await websocket.send("WHAT THE FUCK")


if __name__ == "__main__":
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    cert = pathlib.Path(__file__).parent/"ssl"/"mycert.pem"
    key = pathlib.Path(__file__).parent/"ssl"/"mykey.pem"
    ssl_context.load_cert_chain(cert, key)

    start_server = websockets.serve(hello, "localhost", 8765, ssl=ssl_context)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()