
class Function(object):
    def get_closures(self, arg_count):
        raise NotImplementedError
    
    def call_function(self, dynamic_context, args):
        raise NotImplementedError
    
    def get_min_args(self):
        raise NotImplementedError
    
    def get_max_args(self):
        raise NotImplementedError


class Module(Function):
    def get_function(self, name):
        raise NotImplementedError
    
    def get_default_bind_name(self):
        raise NotImplementedError











































