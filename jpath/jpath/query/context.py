
from copy import copy

class Context(object):
    def new(self, **kwargs):
        new = copy(self)
        for thing in self._things:
            if thing in kwargs:
                setattr(new, thing, kwargs[thing])
        return new


class StaticContext(Context):
    _things = ["module", "function"]
    
    def __init__(self, module, function):
        self.module = module
        self.function = function


class DynamicContext(Context):
    _things = "context_item", "context_position", "context_size"
    
    def __init__(self, context_item, context_position, context_size):
        self.context_item = context_item
        self.context_position = context_position
        self.context_size = context_size


class LocalContext(Context):
    _things = []
    
    def __init__(self):
        self.vars = {}
    
    def new(self, **kwargs):
        new = Context.new(self, **kwargs)
        if "set_name" in kwargs:
            new.vars[kwargs["set_name"]] = kwargs["set_value"]
        if "unset_name" in kwargs:
            del new.vars[kwargs["unset_name"]]
        return new


