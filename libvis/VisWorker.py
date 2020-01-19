import webbrowser
from legimens import App

from .helpers.threaded import threaded
from .http_server import create_server as create_http
from .VisVars import VisVars

class Vis():
    def __init__(self, ws_port = 7700, vis_port=7000, nb_name=None):
        self.ws_port = ws_port
        self.vis_port = vis_port
        self.nb_name = nb_name

        self.http_server = create_http(port=vis_port)

        self.app = App(addr='localhost', port=ws_port)
        self.app.vars = VisVars()
        self.app._register_child(self.app.vars)
        self.vars = self.app.vars

    def start(self):
        self.phttp = threaded( self.http_server.serve_forever, name='http')
        self.app.run()

    def show(self):
        if self.nb_name:
            params = '?p='+self.nb_name
        else: params = ''
        webbrowser.open_new_tab(
            f"localhost:{self.vis_port}/{params}"
        )

    def stop(self):
        print("Stopping app server")
        if self.phttp.is_alive():
            self.http_server.shutdown()
        print("Stopping websocket server")
        self.app.stop()
