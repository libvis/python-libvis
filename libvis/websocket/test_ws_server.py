import time
# Using threading instead of multiprocessing 
# to allow recording received messages
from multiprocessing.dummy import Process

# For some reason trio does not rethrow StopIteration
from trio_websocket import ConnectionClosed
from .ws_server import start_server
from .ws_client import start_client
from .message_gen import async_list, async_gen


def test_simple():
    client_received = []
    server_received = []

    async def server(client_messages):
        yield 'Ping'
        async for message in client_messages:
            print("<<", message)
            server_received.append(message)
            #Listen only for one message
            raise ConnectionClosed('Done all stuff')

    async def client(server_messages):
        async for message in server_messages:
            print(">>", message)
            client_received.append(message)
            # If the following line is outside message loop, 
            # server and client are deadlocked. Someone has to start
            yield 'Pong'

    Process(target=start_server,
            args=('0.0.0.0', 8000, server)
           ).start()
    time.sleep(.1)

    start_client('ws://localhost:8000', client)

    assert client_received[0] == 'Ping'
    assert server_received[0] == 'Pong'

    print(async_list(server(async_gen(['Maca','Waca']))))
    print(async_list(client(async_gen('ahhaehasuh1'))))
