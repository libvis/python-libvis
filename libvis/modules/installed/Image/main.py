from libvis.modules import BaseModule
import colorsys
import PIL
import io
import base64
import numpy as np

class Image(BaseModule):
    """
    A module to display an image from 2- or 3-d numpy matrix

    Args:
        imagedata (numpy.ndarray): Data scaled from 0 to 1

    Note that sending large images frequently can be slow,
    depending on your network connection.

    This table gives an estimate of how often can you have
    updates going on a good network:

    +-----------------+-----------+-------------------+
    | Image size      | Data size | Images per second |
    +=================+===========+===================+
    | 200x200 color   | 36kB      | hundreds          |
    +-----------------+-----------+-------------------+
    | 600x600 color   | 190kB     | tens              |
    +-----------------+-----------+-------------------+
    | 1200x1200 color | 561kB     | several           |
    +-----------------+-----------+-------------------+

    Returns:
            An image object to display in the `libvis` web app
    """
    name="Image"
    def __init__(self, imagedata):
        super().__init__(image=imagedata)

    def update(self, imagedata):
        """ Update image data.
        Instead of creating new ``Images``, use this method for faster updates:
        will queue data for sending immediately.

        Args:
            imagedata: array to update data.
        """
        self.image = imagedata

    def vis_get(self, key):
        """ Convert ``self.image`` to PNG base64-encoded string. """
        #value = super().vis_get(key) # makes {value:preprocess(value), type:self.name}
        value = self[key]
        im = PIL.Image.fromarray(np.uint8(value*255))
        in_mem_file = io.BytesIO()
        im.save(in_mem_file, format='PNG')
        in_mem_file.seek(0)
        imbytes = base64.b64encode(in_mem_file.read())
        return imbytes.decode('ascii')

    @classmethod
    def from_hsv(cls, hue, saturation, value):
        """ Create image from hsv values.

        Args:
            hue: np.ndarray
            saturation: np.ndarray
            value: np.ndarray

        Returns:
            An image object to display in the `libvis` web app
        """

        im = np.array(np.vectorize(colorsys.hsv_to_rgb)(hue, saturation, value))
        im = im.swapaxes(0, -1)
        return cls(im)

    @classmethod
    def test_object(cls):
        """ Create a test object: image of a domain-colored graph of a complex function """
        def f(z):
            k = 3
            return (z**k - 1)/(z**k + 1 + 4j)
        N = 400
        x, y = np.meshgrid(np.linspace(-2, 2, N), np.linspace(-2, 2, N))
        z = f(x + 1j*y)
        scale = lambda x: np.interp(x, (x.min(), x.max()), (0, 1))
        al = .10
        brightness = scale(1 - al**np.abs(z))
        color = scale(np.angle(z))

        return cls.from_hsv(color, 1, brightness)
