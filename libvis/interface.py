import json
from .VisVars import VisVars
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

# -- Configure IFC map: type->serializer

IFC = {}

def add_serializer(type, ser):
    IFC[type] = ser


def reset_IFC():
    """ Reinitialize global value of IFC

    Should I have global IFC or local to Vis obj?
    For:
        Different Vis instances might share set up
        visualization so no need to configure them separately.
    Against:
        Different Vis may serve different purposes,
        so there might be a need to configure them
                differently.
    """
    def __x():
        pass

    IFC.clear()
    add_serializer(type(__x), str)
    add_serializer(type(print), str)

reset_IFC()
# --


def serialize_to_vis(value):
    value, type_= preprocess_value(value)
    return {'value': value, 'type': type_}

def infer_type(val):
    if isinstance(val, VisVars):
        type_ = type(val).name
    else :
        type_ = type(val).__name__
    return type_

def preprocess_value(val):
    try:
        # Note: libvis object is dict and will throw KeyError
        _ = val.vis_repr
        ret, type_ = val.vis_repr()
        return ret, type_

    except (AttributeError, KeyError):
        pass


    if type(val) in IFC.keys():
        type_ = infer_type(val)
        ret = IFC[type(val)](val)
    elif is_bokeh(val):
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
            type_='_img'
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
