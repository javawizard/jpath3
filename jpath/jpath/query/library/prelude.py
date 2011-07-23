
from jpath.query import data as d, exceptions as e, utils
import jpath

def size(dynamic):
    thing = dynamic.context_item
    if not isinstance(thing, (d.List, d.Object)):
        raise e.TypeException("Expected " + str(thing) + " to be a list or object")
    return utils.create_number(dynamic.context_item.get_size())


def position(dynamic):
    return utils.create_number(dynamic.context_position)


def count(dynamic, sequence=None):
    if sequence is None:
        return utils.create_number(dynamic.context_size)
    return sequence.get_size()


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













































