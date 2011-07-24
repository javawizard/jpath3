
from abc import ABCMeta as ABC, abstractmethod as abstract
from jpath.query import utils, exceptions as e
from jpath.sane_total_ordering import total_ordering
import json

def core_type(c):
    c.jpath_type = c
    return c


@total_ordering
class Item(object):
    __metaclass__ = ABC
    
    @abstract
    def get_children(self): pass
    
    @abstract
    def get_pair_children(self): pass
    
    @abstract
    def get_for_pattern(self, pattern): pass
    
    @abstract
    def get_for_pair_pattern(self, pattern): pass
    
    @abstract
    def get_for_indexer(self, value): pass
    
    @abstract
    def get_for_pair_indexer(self, value): pass
    
    @abstract
    def equal(self, other): pass
    
    @abstract
    def less_than(self, other): pass
    
    @abstract
    def to_jpath(self): pass
    
    def to_string(self):
        # I decided to allow everything to be converted to a string and to
        # take its default JPath representation if another conversion is not
        # specified, so this is commented out for now.
        # raise e.TypeException("Trying to convert a value of type " +
        #         str(type(self)) + " to a string, but this type does not "
        #         "support converting itself into a string.")
        return self.to_jpath()
    
    def __eq__(self, other):
        if not isinstance(other, Item):
            return False
        if self.jpath_type != other.jpath_type:
            return False
        return self.equal(other)
    
    def __lt__(self, other):
        if not isinstance(other, Item):
            return NotImplemented
        our_type = self.jpath_type
        other_type = other.jpath_type
        if our_type != other_type: # Not the same JPath type, so we'll return
            # a comparison based on the JPath type to guarantee consistent but
            # arbitrary ordering among JPath types
            return our_type < other_type
        # Same JPath type, so we ask it to do the comparison.
        return self.less_than(other)
    
    @abstract
    def __hash__(self): pass


class IdentityItem(object):
    """
    Provides ordering operation implementations that assume that an item is
    only equal to its identity-wise self. This class is intended to be used
    for items where such behavior makes sense, such as most updates.
    """
    def equal(self, other):
        return self is other
    
    def less_than(self, other):
        return id(self) < id(other)
    
    def __hash__(self):
        return id(self)


class EmptyItem(object):
    """
    Provides implementations of get_for_pattern and family that return the
    empty sequence. This class is intended to be used as a mix-in for items
    where such behavior makes sense, such as most updates (although a lot of
    the update classes override get_for_pattern to provide information about
    the update).
    
    This class's implementation of get_for_indexer delegates to
    get_for_pattern if the value is a string; this can be used to override
    get_for_pattern if pattern behavior is desired.
    """
    def get_children(self): return EmptySequence()
    
    def get_pair_children(self): return EmptySequence()
    
    def get_for_pattern(self, pattern): return EmptySequence()
    
    def get_for_pair_pattern(self, pattern): return EmptySequence()
    
    def get_for_indexer(self, value):
        single = utils.try_single_instance(value, String)
        if single:
            return self.get_for_pattern(single.get_value())
        return EmptySequence()
    
    def get_for_pair_indexer(self, value):
        single = utils.try_single_instance(value, String)
        if single:
            return self.get_for_pair_pattern(single.get_value())
        return EmptySequence()


@total_ordering
class Sequence(object):
    __metaclass__ = ABC
    
    @abstract
    def get_item(self, index): pass
    
    @abstract
    def get_size(self): pass
    
    @abstract
    def is_synthetic(self): pass
    
    def to_jpath(self):
        if self.get_size() == 1:
            return self.get_item(0).to_jpath()
        return "(" + ", ".join(v.to_jpath() for v in self) + ")"
    
    def to_python_list(self):
        """
        Converts this sequence into a Python list. Subclasses can override
        this if they can provide a more efficient implementation.
        """
        return [self.get_item(i) for i in xrange(self.get_size)]
    
    def iterator(self):
        """
        Returns an iterator over this sequence's items. Subclasses can
        override this if they can provide a more efficient implementation.
        """
        for i in xrange(self.get_size()):
            yield self.get_item(i)
    
    def __iter__(self):
        return self.iterator()
    
    def __eq__(self, other):
        if not isinstance(other, Sequence):
            return False
        return self.to_python_list() == other.to_python_list()
    
    def __lt__(self, other):
        if not isinstance(other, Sequence):
            return NotImplemented
        return self.to_python_list() < other.to_python_list()


@core_type
class Number(Item):
    __metaclass__ = ABC
    
    @abstract
    def get_as_float(self): pass
    
    @abstract
    def get_as_int(self): pass
    
    def get_children(self):
        return EmptySequence()
    
    def get_pair_children(self):
        return EmptySequence()
    
    def get_for_pattern(self, pattern):
        return EmptySequence()
    
    def get_for_pair_pattern(self, pattern):
        return EmptySequence()
    
    def get_for_indexer(self, value):
        return EmptySequence()
    
    def get_for_pair_indexer(self, value):
        return EmptySequence()
    
    def equal(self, other):
        return other.get_as_float() == self.get_as_float()
    
    def less_than(self, other):
        return self.get_as_float() < other.get_as_float()
    
    def __hash__(self):
        return hash(self.get_as_float())
    
    def to_jpath(self):
        value = self.get_as_float()
        if int(value) == value: # value is a whole number
            return str(int(value))
        return str(value)


@core_type
class Boolean(Item):
    __metaclass__ = ABC
    
    @abstract
    def get_value(self): pass
    
    def get_children(self):
        return EmptySequence()
    
    def get_pair_children(self):
        return EmptySequence()
    
    def get_for_pattern(self, pattern):
        return EmptySequence()
    
    def get_for_pair_pattern(self, pattern):
        return EmptySequence()
    
    def get_for_indexer(self, value):
        return EmptySequence()
    
    def get_for_pair_indexer(self, value):
        return EmptySequence()
    
    def equal(self, other):
        return other.get_value() == self.get_value()
    
    def less_than(self, other):
        return self.get_value() < other.get_value()
    
    def __hash__(self):
        return hash(self.get_value())
    
    def to_jpath(self):
        return "true" if self.get_value() else "false"


@core_type
class Null(Item):
    __metaclass__ = ABC
    
    def get_children(self):
        return EmptySequence()
    
    def get_pair_children(self):
        return EmptySequence()
    
    def get_for_pattern(self, pattern):
        return EmptySequence()
    
    def get_for_pair_pattern(self, pattern):
        return EmptySequence()
    
    def get_for_indexer(self, value):
        return EmptySequence()
    
    def get_for_pair_indexer(self, value):
        return EmptySequence()
    
    def equal(self, other):
        return True
    
    def less_than(self, other):
        return False
    
    def __hash__(self):
        return 0
    
    def to_jpath(self):
        return "null"


@core_type
class String(Item):
    __metaclass__ = ABC
    
    @abstract
    def get_value(self): pass
    
    def get_children(self):
        return StandardSequence([StandardString(s) for s in self.get_value()])
    
    def get_pair_children(self):
        return EmptySequence()
    
    def get_for_pattern(self, pattern):
        return EmptySequence()
    
    def get_for_pair_pattern(self, pattern):
        return EmptySequence()
    
    def get_for_indexer(self, value):
        index = utils.get_single_instance(value, Number).get_as_int()
        this_value = self.get_value()
        if index < 0 or index >= len(this_value):
            return EmptySequence() # or raise an exception? Check on XQuery's behavior for this
        return StandardSequence([StandardString(this_value[index])])
    
    def get_for_pair_indexer(self, value):
        return EmptySequence()
    
    def equal(self, other):
        return other.get_value() == self.get_value()
    
    def less_than(self, other):
        return self.get_value() < other.get_value()
    
    def __hash__(self):
        return hash(self.get_value())
    
    def to_jpath(self):
        # This is sort of hackish; is it the best way to go about it?
        return json.dumps(self.get_value())
    
    def to_string(self):
        return self.get_value()


@core_type
class List(Item):
    """
    A list.
    
    get_items returns a sequence of all items in this list.
    """
    __metaclass__ = ABC
    
    @abstract
    def get_size(self): pass
    
    @abstract
    def get_item(self, index): pass
    
    @abstract
    def get_items(self): pass
    
    def to_python_list(self):
        """
        Converts this List into a Python list. Subclasses can override this
        if they have a more efficient implementation than simply iterating
        through all the items and building up a Python list.
        """
        return [self.get_item(i) for i in xrange(self.get_size())]
    
    def __iter__(self):
        """
        Returns an iterator over this list's values. Subclasses can override
        this if they can provide a more efficient implementation.
        """
        for i in xrange(self.get_size()):
            yield self.get_item(i)
    
    def get_children(self):
        return StandardSequence([self.get_item(i) for i in xrange(self.get_size())])
    
    def get_pair_children(self):
        return StandardSequence([])
    
    def get_for_pattern(self, pattern):
        return utils.flatten([self.get_item(i).get_for_pattern(pattern) for i in xrange(self.get_size())])
    
    def get_for_pair_pattern(self, pattern):
        return utils.flatten([self.get_item(i).get_for_pair_pattern(pattern) for i in xrange(self.get_size())])
    
    def get_for_indexer(self, value):
        if value.get_size() == 1:
            single = value.get_item(0)
            if isinstance(single, Number):
                number = single[0].get_as_int()
                if number >= 0 and number < self.get_size():
                    return StandardSequence([self.get_item(number)])
                else:
                    return StandardSequence([])
        return utils.flatten([self.get_item(i).get_for_indexer(value) for i in xrange(self.get_size())])
    
    def get_for_pair_indexer(self, value):
        return utils.flatten([self.get_item(i).get_for_pair_indexer(value) for i in xrange(self.get_size())])
    
    def equal(self, other):
        if self.get_size() != other.get_size():
            return False
        for i in xrange(self.get_size()):
            if not self.get_item(i).equal(other.get_item(i)):
                return False
        return True
    
    def less_than(self, other):
        return self.to_python_list() < other.to_python_list()
    
    def __hash__(self):
        return hash([self.get_item(i) for i in xrange(self.get_size())])
    
    def to_jpath(self):
        return "[" + ", ".join(v.to_jpath() for v in self) + "]"


@core_type
class Pair(Item):
    __metaclass__ = ABC
    
    @abstract
    def get_key(self): pass
    
    @abstract
    def get_value(self): pass
    
    def __iter__(self):
        """
        Returns an iterator that yields exactly two items: the key of this
        Pair and the value of this Pair. Subclasses can override this if they
        can provide a more efficient implementation.
        """
        yield self.get_key()
        yield self.get_value()
    
    def get_children(self):
        return StandardSequence([])
    
    def get_pair_children(self):
        return StandardSequence([])
    
    def get_for_pattern(self, pattern):
        if pattern == "key" or pattern == "name":
            return StandardSequence([self.get_key()])
        if pattern == "value":
            return StandardSequence([self.get_value()])
        return StandardSequence([])
    
    def get_for_pair_pattern(self, pattern):
        return StandardSequence([])
    
    def get_for_indexer(self, value):
        if value.get_size() == 1:
            if isinstance(value.get_item(0), String):
                return self.get_for_pattern(value.get_item(0).get_value())
        return StandardSequence([])
    
    def get_for_pair_indexer(self, value):
        return StandardSequence([])
    
    def equal(self, other):
        if not isinstance(other, Pair):
            return False
        return self.get_key().equal(other.get_key()) and self.get_value().equal(other.get_value())
    
    def less_than(self, other):
        self_key = self.get_key()
        other_key = other.get_key()
        if self_key < other_key:
            return True
        if other_key < self_key:
            return False
        # Keys are equal, so check values
        return self.get_value() < other.get_value()
    
    def __hash__(self):
        return hash(self.get_key()) ^ hash(self.get_value())
    
    def to_jpath(self):
        return self.get_key().to_jpath() + ": " + self.get_value().to_jpath()


@core_type
class Object(Item):
    """
    An object.
    
    get_values and get_pairs return Sequence objects containing the
    values/pairs.
    """
    __metaclass__ = ABC
    
    @abstract
    def get_value(self, key): pass
    
    @abstract
    def get_pair(self, key): pass
    
    @abstract
    def get_values(self): pass
    
    @abstract
    def get_pairs(self): pass
    
    @abstract
    def get_size(self): pass
    
    def to_python_dict(self):
        """
        Same as List.to_python_list, but for Objects, and converts them to a
        Python dict.
        """
        return dict([(p.get_key(), p.get_value()) for p in self.get_pairs()])
    
    def __iter__(self):
        """
        Returns an iterator over this object's pairs. Subclasses can override
        this if they can provide a more efficient implementation.
        """
        pairs = self.get_pairs()
        for v in pairs: # pairs is a sequence, and sequences are also
            # iterable. TODO: consider changing this to return iter(pairs).
            yield v
    
    def get_children(self):
        return self.get_values()
    
    def get_pair_children(self):
        return self.get_pairs()
    
    def get_for_pattern(self, pattern):
        value = self.get_value(StandardString(pattern))
        if value is None:
            return EmptySequence()
        return utils.singleton(value)
    
    def get_for_pair_pattern(self, pattern):
        value = self.get_pair(StandardString(pattern))
        if value is None:
            return EmptySequence()
        return utils.singleton(value)
    
    def get_for_indexer(self, value):
        result = self.get_value(utils.get_single(value))
        if result is None:
            return EmptySequence()
        return utils.singleton(result)
    
    def get_for_pair_indexer(self, value):
        result = self.get_pair(utils.get_single(value))
        if result is None:
            return EmptySequence()
        return utils.singleton(result)
    
    def equal(self, other):
        return self.to_python_dict() == other.to_python_dict()
    
    def less_than(self, other):
        return self.to_python_dict() < other.to_python_dict()
    
    def __hash__(self):
        return hash(self.to_python_dict())
    
    def to_jpath(self):
        return "{" + ", ".join(v.to_jpath() for v in self) + "}"


class Update(Item):
    __metaclass__ = ABC


@core_type
class Insert(EmptyItem, IdentityItem, Update):
    __metaclass__ = ABC
    
    @abstract
    def get_value(self):
        """
        Returns the value that this insertion should insert.
        """
    
    @abstract
    def get_reference(self):
        """
        Returns the reference. For "insert x ... into y", this is the list or
        dict into which get_value() should be inserted. For "insert x before
        y" or "insert x after y", this is the value relative to which
        get_value() should be inserted.
        """
    
    @abstract
    def get_position(self):
        """
        Returns the position at which this value should be inserted. This is
        either the string "start", the string "end", the string "before", the
        string "after", an int to indicate a numerical position, or None to
        indicate an unspecified "insert x into y".
        """
    
    def to_jpath(self):
        result = "insert " + self.get_value().to_jpath() + " "
        ref = self.get_reference().to_jpath()
        position = self.get_position()
        if position == "before":
            result += "before " + ref
        elif position == "after":
            result += "after " + ref
        elif position == "start":
            result += "at start into " + ref
        elif position == "end":
            result += "at end into " + ref
        else:
            result += "at position " + str(position) + " into " + ref
        return result


@core_type
class Delete(EmptyItem, IdentityItem, Update):
    __metaclass__ = ABC
    
    @abstract
    def get_value(self): pass
    
    def to_jpath(self):
        return "delete value " + self.get_value().to_jpath()


@core_type
class Replace(EmptyItem, IdentityItem, Update):
    __metaclass__ = ABC
    
    @abstract
    def get_target(self):
        """
        Returns the value which is to be replaced.
        """
    
    @abstract
    def get_replacement(self):
        """
        Returns the value which is to replace get_target().
        """
    
    def to_jpath(self):
        return ("replace value " + self.get_target().to_jpath()
                + " with " + self.get_replacement().to_jpath())


class EmptySequence(Sequence):
    def get_item(self, index):
        raise IndexError
    
    def get_size(self):
        return 0
    
    def is_synthetic(self):
        return False
    
    def __repr__(self):
        return "EmptySequence()"
    
    def to_python_list(self):
        return []


class StandardSequence(Sequence):
    def __init__(self, values):
        if not isinstance(values, (list, tuple)):
            raise Exception("values is %s" % repr(values))
        self.values = values
    
    def get_item(self, index):
        return self.values[index]
    
    def get_size(self):
        return len(self.values)
    
    def is_synthetic(self):
        return False
    
    def __repr__(self):
        return "StandardSequence(%s)" % repr(self.values)
    
    def to_python_list(self):
        return self.values
    
    def iterator(self):
        return self.values.__iter__()


class StandardString(String):
    def __init__(self, value):
        self.value = value
    
    def get_value(self):
        return self.value
    
    def __repr__(self):
        return "StandardString(%s)" % repr(self.value)


class StandardNumber(Number):
    def __init__(self, value):
        self.value = value
    
    def get_as_float(self):
        return float(self.value)
    
    def get_as_int(self):
        return int(self.value)
    
    def __repr__(self):
        return "StandardNumber(%s)" % repr(self.value)


class StandardBoolean(Boolean):
    def __init__(self, value):
        self.value = value
    
    def get_value(self):
        return self.value
    
    def __repr__(self):
        return "StandardBoolean(%s)" % self.value


class StandardNull(Null):
    def __repr__(self):
        return "StandardNull()"


class StandardList(List):
    def __init__(self, list):
        self.list = list
    
    def get_size(self):
        return len(self.list)
    
    def get_item(self, index):
        return self.list[index]
    
    def get_items(self):
        return StandardSequence(self.list)
    
    def __repr__(self):
        return "StandardList(%s)" % repr(self.list)
    
    def to_python_list(self):
        return self.list


class StandardPair(Pair):
    def __init__(self, key, value):
        self.key = key
        self.value = value
    
    def get_key(self):
        return self.key
    
    def get_value(self):
        return self.value
    
    def __repr__(self):
        return "StandardPair(%s, %s)" % (repr(self.key), repr(self.value))


class StandardObject(Object):
    def __init__(self, value):
        self.pair_dict = {}
        self.value_dict = {}
        if not isinstance(value, (Sequence, list, tuple)):
            raise Exception(type(value))
        for p in value:
            if not isinstance(p, Pair):
                raise Exception(type(p))
            k = p.get_key()
            self.pair_dict[k] = p
            self.value_dict[k] = p.get_value()
    
    def get_value(self, key):
        return self.value_dict.get(key, None)
    
    def get_values(self):
        return StandardSequence(self.value_dict.values())
    
    def get_pair(self, key):
        return self.pair_dict.get(key, None)
    
    def get_pairs(self):
        return StandardSequence(self.pair_dict.values())
    
    def get_size(self):
        return len(self.pair_dict)
    
    def __repr__(self):
        return "StandardObject(%s)" % self.get_pairs().to_python_list()
    
    def to_python_dict(self):
        return self.value_dict


class StandardInsert(Insert):
    def __init__(self, value, reference, position):
        """
        Creates a new insertion. (value, reference, position) are,
        respectively, thus for these different forms of the insert statement:
        
        insert x before y: (x, y, "before")
        insert x after y: (x, y, "after")
        insert x at start into y: (x, y, "start")
        insert x at end into y: (x, y, end)
        insert x at position y into z: (x, z, y)
        """
        self.value = value
        self.reference = reference
        self.position = position
    
    def get_value(self):
        return self.value
    
    def get_reference(self):
        return self.reference
    
    def get_position(self):
        return self.position
    
    def __repr__(self):
        return "StandardInsert(%s, %s, %s)" % (repr(self.value),
                repr(self.reference), repr(self.position))


class StandardDelete(Delete):
    def __init__(self, value):
        self.value = value
    
    def get_value(self):
        return self.value
    
    def __repr__(self):
        return "StandardDelete(%s)" % repr(self.value)


class StandardReplace(Replace):
    def __init__(self, target, replacement):
        self.target = target
        self.replacement = replacement
    
    def get_target(self):
        return self.target
    
    def get_replacement(self):
        return self.replacement
    
    def __repr__(self):
        return "StandardReplace(%s, %s)" % (repr(self.target), repr(self.replacement))


del core_type



































