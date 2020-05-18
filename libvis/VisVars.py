from legimens import Object
from . import interface as ifc

class VisVars(Object):
    name='VisVar'
    def _prepare_send(self, name, value):
        o = ifc.serialize_to_vis(value)
        # Make sure that any nested children that are objects
        # are converted to ref(object)
        name, value = super()._prepare_send(name, o)
        return name, value

class VisObject(VisVars):
    name='VisVar'
    def __init__(self, value):
        super().__init__()
        self.body = value
