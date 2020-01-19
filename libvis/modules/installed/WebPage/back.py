from libvis.modules import BaseModule
import json

class WebPage(BaseModule):
    name="WebPage"
    def serial(self):
        return json.dumps({'addr':self.address})
