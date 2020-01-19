import trio
from sys import stderr
from trio_websocket import open_websocket_url, ConnectionClosed
from .message_gen import message_gen

def main(addr='wss://echo.websocket.org', message='hello world'):
    trio.run(send_one, addr, message)

async def communicate(addr, iterable_fn):
    try:
        async with open_websocket_url(addr) as ws:

            async for message in iterable_fn(message_gen(ws)):
                try:
                    await ws.send_message(message)
                except ConnectionClosed:
                    print('ConnectionClosed while sending')
                    return

    except OSError as ose:
        print('Connection attempt failed: %s' % ose, file=stderr)

def start_client(addr, iterable_fn):
    print('Starting client')
    try:
        trio.run(communicate, addr, iterable_fn)
    except StopIteration:
        return

def _default_on_error(err):
    print('Connection failed: %s'%err)

async def open_ws_wrapper(addr,on_connect, on_error=_default_on_error):
    try:
        async with open_websocket_url(addr) as ws:
            on_connect(ws)
    except OSError as ose:
        on_error(ose)
    except ConnectionClosed as e:
        on_error(e)

async def send_one(addr, message):
    try:
        async with open_websocket_url(addr) as ws:
            await ws.send_message(message)
            message = await ws.get_message()
            print('Received message: %s' % message)
    except OSError as ose:
        print('Connection attempt failed: %s' % ose, file=stderr)

async def send_iter(addr, iterable):
    try:
        async with open_websocket_url(addr) as ws:
            for message in iterable:
                await ws.send_message(message)
    except OSError as ose:
        print('Connection attempt failed: %s' % ose, file=stderr)


if __name__=="__main__":
    main()
