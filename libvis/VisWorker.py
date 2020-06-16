import webbrowser
from legimens import App
from loguru import logger as log
import time
import sys

from libvis import ref
from .helpers.threaded import threaded
from .http_server import create_server as create_http
from .VisVars import VisVars, VisObject
from .interface import add_serializer, serialize_to_vis

class Vis():
    def __init__(self, ws_port = 7700, vis_port=7000
                 , nb_name=None
                 , debug=False
                ):

        self.ws_port = ws_port
        self.vis_port = vis_port

        if debug: log_level = 'DEBUG'
        else: log_level = 'ERROR'
        self.configure_logging(log_level)
        self.nb_name = nb_name

        self.app = App(addr='localhost', port=ws_port)
        self.app.vars = VisVars()
        self.app._register_child(self.app.vars)
        self.app.serialize_value = serialize_to_vis
        self.vars = self.app.vars

        self.start()


    def start(self):
        """
        Main entry point of legimens.
        Called upon initialization of this class.

        1. Starts an http server with dashboard app
            on `vis_port`.
        2. Starts the legimens app using `vis.app.run()`.


        Raises:
            Exception: Something went wrong when starting
                http or websocket server in legimens.

        """
        self.http_server = create_http(port=self.vis_port)
        if self.http_server is None:
            raise Exception("http server not initialized. Recreate Vis instance.")
        self.phttp = threaded( self.http_server.serve_forever, name='http')
        print(f'Started libvis app at http://localhost:{self.vis_port}')
        self.app.run()

    def use(type_, serializer):
        add_serializer(type_, serializer)

    def watch(self, obj, key, serializer=None):
        o = VisObject(obj)
        self.app.watch_obj(o)
        self.vars[key] = o
        if serializer:
            # Note: this will act on *any* object of the same type
            self.use(type(obj), serializer)
        return ref(o)

    def show(self):
        """ Open libvis dashboard in browser. """

        if self.nb_name:
            params = '?p='+self.nb_name
        else: params = ''
        webbrowser.open_new_tab(
            f"http://localhost:{self.vis_port}/{params}"
        )

    def configure_logging(self, level, sink=sys.stderr):
        log.remove()
        log.add(sink, level=level)

    def stop_http(self):
        if hasattr(self, 'phttp'):
            if self.phttp.is_alive():
                self.http_server.shutdown()
                self.http_server.server_close()
                self.phttp.join()
        else:
            print('Warning: no http server to stop.')

    def stop(self):
        print("Stopping app server...", end="", flush=True)
        self.stop_http()
        print(" OK")
        print("Stopping websocket server...", end="", flush=True)
        self.app.stop()
        print(" OK")

