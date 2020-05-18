from libvis import Vis, ref
from libvis.interface import IFC
import json
import asyncio
from functools import wraps
from mock import patch
import gc

def sync(coro):
    @wraps(coro)
    def wrapper(*args, **kwargs):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(coro(*args, **kwargs))
    return wrapper

@sync
async def test_set_watch():
    x = [5]
    vis = Vis()
    ref_x = vis.watch(x, 'somekey')

    async for msg in vis.app._handle_obj_ref(None, ref(vis.vars)):
        ev = json.loads(msg)
        assert 'somekey' in ev.keys()
        assert ev['somekey']['type'] == 'Object'
        assert ev['somekey']['value'] == ref_x
        break

    async for msg in vis.app._handle_obj_ref(None, ref_x):
        ev = json.loads(msg)
        assert 'body' in ev.keys()
        assert ev['body']['type'] == 'raw'
        assert ev['body']['value'] == x
        break

    # test waiting 
    vis.app._sleep_func = asyncio.sleep
    with patch('legimens.App._send_message_to_subscribers') as send_mock:
        asyncio.ensure_future(vis.app._poll_objects())
        await asyncio.sleep(.5)
        assert send_mock.call_count >= 2

    # test that it collects the garbage
    del x
    del vis.vars['somekey']
    gc.collect()
    await asyncio.sleep(.1)

    async for msg in vis.app._handle_obj_ref(None, ref(vis.vars)):
        ev = json.loads(msg)
        assert 'somekey' not in ev.keys()
        assert len(list(vis.app._child_obj.keys())) == 1
        break

