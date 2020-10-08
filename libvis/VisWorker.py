import webbrowser
from legimens import App
from loguru import logger as log
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
                 , allow_remote=False
                ):

        self.ws_port = ws_port
        self.vis_port = vis_port

        if debug: log_level = 'DEBUG'
        else: log_level = 'ERROR'
        self.nb_name = nb_name

        self.addr = '0.0.0.0' if allow_remote else 'localhost'

        self.app = App(addr=self.addr, port=ws_port)
        self.app.vars = VisVars()
        self.app._register_child(self.app.vars)
        self.app.serialize_value = serialize_to_vis
        self.vars = self.app.vars

        self.configure_logging(log_level)
        self.start()


    # -- Starts

    def start(self):
        """ Start visualization process.

        Main entry point of legimens.
        Called upon initialization of this class.

        1. Starts an http server with dashboard app on `vis_port`.
        2. Starts the legimens app using `Vis.app.run()`.


        Raises:
            Exception: Something went wrong when starting
                http or websocket server in legimens.
        """
        try:
            self.start_http(self.addr, self.vis_port)
        except Exception as e:
            print(f"Webapp HTTP server failed to start at {self.addr}:{self.vis_port}."
                  " To start manually: `Vis.start_http(port)`."
                  " Error was:", e
                  , file=sys.stderr)

        if not self.app._running:
            self.app.run()
        else:
            print("Legimens app is already running, what are you doing? To stop: `Vis.stop()`")

    def start_http(self, addr=None, port=None):
        """ Start the http server on `addr` and `port`. """
        if port is None: port=self.vis_port
        if addr is None: port=self.addr
        self.http_server = create_http(port=port, addr=addr)
        self.phttp = threaded( self.http_server.serve_forever, name='http')
        print(f'Started libvis app at http://{addr}:{port}')

    # --

    def use(self, type_, serializer):
        """ Add a serializer to :meth:`libvis.interface.IFC`. """
        add_serializer(type_, serializer)

    def watch(self, obj, key, serializer=None):
        """ Sets `libvis` to watch an object.

        Parameters:
            obj: the object to watch, has to be serializable.
            key (str): name of the object variable.
            serializer (callable): optional function that converts objects of type(obj) to serializable.

        For sending updates we can use existing channel created for ``vis.vars``,
        but this would introduce overhead. Hence, a new channel is created
        by creating a :meth:`libvis.VisVars.VisObject` of type :meth:`legimens.Object`.
        It is a wrapper that has single ``body`` attribute.
        Legimens will send serialized :meth:`legimens.Object` every ``vis.app._watch_poll_delay`` seconds.

        Returns `ref` of the proxy ``VisObject``.
        """
        proxy_obj = VisObject(obj)
        self.app.watch_obj(proxy_obj)
        # it will register. is it bad?
        self.vars.__setattr__(key, proxy_obj)
        if serializer:
            # Note: this will act on *any* object of the same type
            self.use(type(obj), serializer)
        return ref(proxy_obj)

    def show(self):
        """ Open libvis dashboard in browser. """

        if self.nb_name:
            params = '?p='+self.nb_name
        else: params = ''
        webbrowser.open_new_tab(
            f"http://{self.addr}:{self.vis_port}/{params}"
        )

    def configure_logging(self, level, sink=sys.stderr):
        """ Sets up logging verbosity.

        Args:
            level (str):
                ERROR, WARNING, INFO, DEBUG, TRACE
            sink: stream or file for logs
        """

        log.remove()
        log.add(sink, level=level)

    # -- Stops

    def stop_http(self):
        """ Stops the http threaded server. """
        if hasattr(self, 'phttp'):
            if self.phttp.is_alive():
                self.http_server.shutdown()
                self.http_server.server_close()
                self.phttp.join()
        else:
            print('Warning: no http server to stop.')

    def stop(self):
        print("Stopping webapp http server: `Vis.stop_http()`...", end="", flush=True)
        self.stop_http()
        print(" OK")
        print("Stopping websocket server: `Vis.app.stop()`...", end="", flush=True)
        self.app.stop()
        print(" OK")

    # --
