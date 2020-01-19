import json
from webvis.VisVars import VisVars
try:
    import numpy as np
    import matplotlib
    import mpld3
    import bokeh
    #mpld3 hack
    from mpld3 import _display
    class NumpyEncoder(json.JSONEncoder):
        def default(self, obj):
            import numpy as np
            if isinstance(obj, np.ndarray):
                return obj.tolist()
            return json.JSONEncoder.default(self, obj)
    _display.NumpyEncoder = NumpyEncoder
except Exception as e:
    print(e)

def preprocess_value(val):
    if is_bokeh(val):
        ret = bokeh.embed.file_html(val, bokeh.resources.Resources('cdn'))
        type_ = 'mpl'
    elif is_mpl(val):
        ret = mpld3.fig_to_html(val)
        type_ = 'mpl'
    elif is_numpy(val):
        ret, type_ = ndarray_val(val)
    elif isinstance(val, VisVars):
        ret, type_ = vismodule_val(val)
    else:
        ret = val
        type_ = 'raw'

    return ret, type_

def vismodule_val(val):
    ret = val._ref()
    type_ = val.name
    return ret, type_

def ndarray_val(val):
    sh = val.shape
    ret = None
    if len(sh) >= 2:
        if sh[0]>10 and sh[1]>10:
            ret = numpy_to_image(val)
            type_='img'
        else:
            ret = val.tolist()
            type_ = 'raw'
    else:
        ret = val.tolist()
        type_ = 'raw'
    return ret, type_

def numpy_to_image(val):
    sh = val.shape
    alpha = np.ones(list(sh[:2])+[1])*255
    if len(sh)==2:
        # Grayscale image
        val = val.reshape(sh[0],-1,1)
        val = np.concatenate((val,val,val,alpha),axis = -1)
    if len(sh)==3:
        # Color image
        val = np.concatenate((val,alpha), axis=-1)
    val = val.flatten()
    ret = list(sh[:2]) + val.tolist()
    return ret

def _siletly_catch_return_false(f):
    def g(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception:
            return False
    return g

@_siletly_catch_return_false
def is_mpl(val):
    return isinstance(val, matplotlib.figure.Figure)
@_siletly_catch_return_false
def is_bokeh(val):
    return isinstance(val,bokeh.model.Model) or isinstance(val,bokeh.document.document.Document)
@_siletly_catch_return_false
def is_numpy(val):
    return isinstance(val, np.ndarray)
