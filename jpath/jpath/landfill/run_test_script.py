
from jpath.query import interpreter, context
from jpath.query.data import StandardNull
from jpath.query.utils import create_number
import os

if __name__ == "__main__":
    i = interpreter.Interpreter()
    i.get_binder("jpath").add_path(os.path.expanduser("~"))
    m = i.bind_module("jpath", "/test.jpath")
    print "\nQuery result was: " + str(m.call_function(context.DynamicContext(
            StandardNull(), create_number(0), create_number(0)), []))
