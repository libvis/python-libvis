from libvis.modules import BaseModule
from libvis import interface as ifc
import numpy as np
import json

class Gallery(BaseModule):
    name="Gallery"
    def __init__(self, images, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.images = images

    def vis_get(self, key):
        try:
            value = super().vis_get(key) # makes {value:preprocess(value), type:self.name}
            value = [ifc.serialize_to_vis(x) for x in value]

            print('In vis_get of Gallery: ', key, value)
        except Exception as e:
            print('In vis_get of Gallery: ', key, e)
            return 'Error'

        return value

    def vis_set(self, key, value):
        super().vis_set(key, value) # same as self[key] = value
        print('updated value form front: ', key, value)

    @classmethod
    def test_object(cls):
        from libvis.modules import Image
        def test_image(k):
            r = 2
            a, b = np.linspace(0, 1*r, 100), np.linspace(0, .6*r, 60)
            x, y = np.meshgrid(a, b)
            return x*y+np.sin(k*x)
        N = 4
        images =  [Image(test_image(x)) for x in range(N)]
        images += [np.sin(np.linspace(0, 12, 20))]
        return cls(images)
