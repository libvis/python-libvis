from webvis import VisVars
import json

class BaseModule(VisVars):
    def vis_get(self, key):
        value = self[key]
        name, value = super()._prepare_send(name, value)
        return value

    def vis_set(self, key, value):
        super()._prepare_set(key, value)

    def _prepare_send(self, name, value):
        value = self.vis_get(name)
        return name, value

    def _commit_update(self, name, value):
        self.vis_set(name, value)

class BaseTestModule(VisVars):
    @classmethod
    def test_object(cls, *args, **kwargs):
        return cls()



