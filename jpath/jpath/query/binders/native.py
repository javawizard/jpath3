
from jpath.query import binder, module, data, exceptions, utils

class NativeBinder(binder.Binder):
    default_name = "native"
    
    def __init__(self):
        self.module_cache = {}
    
    def bind_module(self, name):
        if name in self.module_cache:
            return self.module_cache[name]
        module = NativeModule(name)
        self.module_cache[name] = module
        return module


class NativeModule(module.Module):
    def __init__(self, name):
        self.name = name
        self.last_name = name.rsplit(".", 1)[-1]
        self.py_module = __import__(name, {}, {}, [self.last_name])
    
    def get_default_bind_name(self):
        return self.last_name
    
    def get_function(self, name):
        function = getattr(self.py_module, name, None)
        if function is None:
            function = getattr(self.py_module, name + "_", None)
        if function is None:
            raise exceptions.FunctionLookupException("No such function " + name + " on native module " + self.name)
        # TODO: have this cache NativeFunction objects, which should make it
        # run a bit faster
        return NativeFunction(self, name, function)


class NativeFunction(module.Function):
    def __init__(self, module, name, py_function):
        self.module = module
        self.name = name
        self.py_function = py_function
    
    def get_min_args(self):
        return 0
    
    def get_max_args(self):
        return 1024 # arbitrary
    
    def get_closures(self, arg_count):
        return [False] * arg_count
    
    def call_function(self, dynamic, args):
        result = self.py_function(dynamic, *args)
        if result is None:
            result = utils.singleton(data.StandardNull())
        if not isinstance(result, data.Sequence):
            raise Exception("Native function " + self.name + " in module "
                    + self.module.name + " didn't return a Sequence object")
        return result





























