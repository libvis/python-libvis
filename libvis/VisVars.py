from legimens import Object
from . import interface as ifc

class VisVars(Object):
    name='VisVar'
    def _prepare_send(self, name, value):
        value, type_= ifc.preprocess_value(value)
        o = {'value': value, 'type': type_}
        name, value = super()._prepare_send(name, o)
        return name, value
