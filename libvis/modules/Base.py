from libvis import VisVars

class BaseModule(VisVars):
    def vis_get(self, key):
        value = self[key]
        """
        If one wants to process the attribute of the module, tey should use
        ifc.serialize_to_vis(value)
        by their own.
        """
        # name, value = super()._prepare_send(key, value)
        return value

    def vis_set(self, key, value):
        super()._commit_update(key, value)

    def _prepare_send(self, name, value):
        value = self.vis_get(name)
        return name, value

    def _commit_update(self, name, value):
        self.vis_set(name, value)

class BaseTestModule(VisVars):
    @classmethod
    def test_object(cls, *args, **kwargs):
        return cls()



