from trio_websocket import ConnectionClosed
import logging as log
#log.basicConfig(level=log.DEBUG)

async def message_gen(ws):
    while True:
        try:
            msg = await ws.get_message()
            log.debug("Got message: %s"% msg)
            yield msg
        except ConnectionClosed:
            log.info('ConnectionClosed while reading')
            return

def async_list(agen):
    import asyncio
    l = []
    async def iter():
        async for x in agen:
            l.append(x)

    try:
        asyncio.run(iter())
    except ConnectionClosed:
        pass
    return l
async def async_gen(l):
    for x in l:
        yield x
