class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)

    def __getattr__(self, name):
        return self[name]

    def __setattr__(self,  name, value):
        self[name] = value

class AttrCbDict(AttrDict):
    def __init__(self, *args, get_cb=print, set_cb=print, **kwargs):
        super(AttrDict, self).__init__(*args, __set=set_cb, __get=get_cb, **kwargs)

    def __getattr__(self, name):
        self['__get'](name)
        return super().__getattr__(name)

    def __setattr__(self, name, value):
        self['__set'](name, value)
        super().__setattr__(name, value)
