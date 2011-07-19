
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













































