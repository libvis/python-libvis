import trio
import sys
from trio_websocket import serve_websocket, ConnectionClosed
from logging import getLogger
from .message_gen import message_gen

log = getLogger("Websocket")

class StopServer(Exception):
    pass

async def ws_serve(addr, port, iterable_fn, on_connect=lambda x:None, nursery=None):
    async def server(request):

        ws = await request.accept()
        on_connect(ws)

        async for message in iterable_fn(message_gen(ws)):
            try:
                await ws.send_message(message)
            except ConnectionClosed:
                log.warning("Connection closed")
                break

    try:
        await serve_websocket(server, addr, port, ssl_context=None, handler_nursery=nursery)
    except OSError as ose:
        print(f"Websocket start on {port} failed: {ose}", file=sys.stderr)
        return
    log.info("Websocket terminates")

def start_server(addr, port, handler_func=print, on_connect=lambda x: None):
    log.info(f"Starting ws server at {addr}:{port}")
    try:
        trio.run(ws_serve, addr, port, handler_func, on_connect)
    except ConnectionClosed as e:
        log.warning(f"Connection closed: {e}")
        return

def start_server_handler(addr, port, handler_func):
    async def handler(client_messages):
        async for message in client_messages:
            yield str(handler_func(message))
    start_server(addr, port, handler)

def stop():
    print("You found a stub!")

def main():
    start_server('127.0.0.1',8000)

if __name__=='__main__':
    main()
