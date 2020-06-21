import gc
import json
import pytest
import asyncio
from mock import patch
from functools import wraps

from libvis import Vis, ref, VisVars
from libvis.interface import IFC

@pytest.mark.asyncio
async def test_set_watch():
    x = [5]
    vis = Vis()
    try:
        ref_x = vis.watch(x, 'somekey')
        assert 'somekey' in vis.vars
        assert isinstance(vis.vars['somekey'] , VisVars)
        # There may be a bug: pytest launches tests common env, but IFC is global. This means that we might have a serializer for np.array in IFC.
        # assert len(IFC.keys()) == 2

        async for msg in vis.app._handle_obj_ref(None, ref(vis.vars)):
            ev = json.loads(msg)
            assert 'somekey' in ev.keys()
            assert ev['somekey']['type'] == 'VisVar'
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
    finally:
        vis.stop()

