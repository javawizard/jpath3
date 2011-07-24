
from jpath.query import data as d, exceptions as e, utils
import jpath

_functions = {}

def m(name):
    def decorator(function):
        _functions[name] = function
        return function
    return decorator


def size(dynamic):
    thing = dynamic.context_item
    if not isinstance(thing, (d.List, d.Object)):
        raise e.TypeException("Expected " + str(thing) + " to be a list or object")
    return utils.create_number(dynamic.context_item.get_size())


def position(dynamic, check=None):
    if check is None:
        return utils.create_number(dynamic.context_position)
    return utils.create_boolean(
            utils.get_single_instance(check, d.Number).get_as_int() == dynamic.context_position)


def count(dynamic, sequence=None):
    if sequence is None:
        return utils.create_number(dynamic.context_size)
    return sequence.get_size()


def first(dynamic):
    return utils.create_boolean(dynamic.context_position == 1)


def last(dynamic):
    return utils.create_boolean(dynamic.context_position == dynamic.context_size)


def print_(dynamic, value):
    print utils.get_single_instance(value, d.String).get_value()


def input(dynamic):
    return utils.singleton(d.StandardString(raw_input()))


def root(dynamic):
    function = dynamic.userland.get("db.get_root", None)
    if function is None:
        raise e.OtherException("Query is not running in the context of a "
                "database, so the root function cannot be called. "
                "Specifically, the dynamic context userland does not have an "
                "entry named db.get_root; this should be a function that "
                "returns the root database object.")
    root = function()
    if not isinstance(root, d.Item):
        raise e.OtherException("Dynamic context userland db.get_root "
                "function returned a value that was not an instance of Item; "
                "specifically, it was an instance of " + str(type(root)))
    return utils.singleton(root)


def cat(dynamic, *args):
    results = []
    for item in (v for arg in args for v in arg): # Iterate over arguments and
        # the items in each of the arguments (which will be a Sequence)
        if not isinstance(item, d.String):
            raise e.TypeException("A value passed to the cat function was "
                    "not a string; it was " + str(type(item)) + ". All "
                    "values passed to cat() must be strings. Consider using "
                    "string() to convert other values to strings.")
        results.append(item.get_value())
    return "".join(results)


@m("get-module")
def _get_module(dynamic, name):
    pass

@m("bind-module")
def _bind_module(dynamic, binder, name):
    pass


@m("get-function")
def _get_function(dynamic, module, name):
    pass


del m













































