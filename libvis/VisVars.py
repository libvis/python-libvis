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

class VisHooks(VisVars):
    name='VisVar'
    def __init__(self, value):
        super().__init__()
        self.body = value

    def on_receive(self, func):
        def _commit_update(update):
            func(update)
        self._commit_update = _commit_update

    def set_serializer(self, ser):
        def _prepare_send(name, value):
            return name, ser(value)
        self._prepare_send = _prepare_send
