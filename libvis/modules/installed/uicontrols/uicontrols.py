
from libvis.modules import BaseModule
from libvis.interface import serialize_to_vis
import json
from .utils import random_quote

class Button(BaseModule):
    name="uicontrols"
    def __init__(self,label='My Button', on_press=print):
        super().__init__(label=label, on_press=on_press)
        self.depressed = False
        self.type='button'

    def vis_set(self, key, value):
        if key == 'depressed':
            if self.depressed:
                if value is False:
                    self.on_press()
        self.depressed = value

    def vis_get(self, key):
        if key == 'on_press':
            return 'function'
        return self[key]

class Slider(BaseModule):
    name="uicontrols"
    def __init__(self, value=4
                 ,min = 0
                 ,max = 10
                 ,on_change=print):
        super().__init__(
            on_change=on_change,
            min=min, max=max, value=value
        )
        self.type='slider'

    def vis_set(self, key, value):
        if key == 'value':
            slider_value = float(value)
            self.on_change(slider_value)
            self.value = slider_value

    def vis_get(self, key):
        tv = serialize_to_vis(self[key])
        return tv['value']


def test_object():
    button =  Button(on_press=print)
    def on_press():
        button.label = button.label[::-1]
    button.on_press = on_press
    #return button

    slider =  Slider()
    def on_change(value):
        print('slider val', value)
        slider.value = value
    slider.on_change = on_change
    return slider
