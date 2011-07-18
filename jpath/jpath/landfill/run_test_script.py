
from jpath.query import interpreter, context
import os

if __name__ == "__main__":
    i = interpreter.Interpreter()
    i.get_binder("jpath").add_path(os.path.expanduser("~"))
    m = i.bind_module("jpath", "/test.jpath")
    f = m.get_function("example")
    print f
    print f.call_function(context.DynamicContext(None, None, None), [])
