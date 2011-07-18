
from abc import ABCMeta as ABC, abstractmethod as abstract
from jpath.query import utils

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


class Sequence(object):
    __metaclass__ = ABC
    
    @abstract
    def get_item(self, index): pass
    
    @abstract
    def get_size(self): pass
    
    @abstract
    def is_synthetic(self): pass


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


class EmptySequence(Sequence):
    def get_item(self, index):
        raise IndexError
    
    def get_size(self):
        return 0
    
    def is_synthetic(self):
        return False
    
    def __repr__(self):
        return "EmptySequence()"


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


class StandardString(String):
    def __init__(self, value):
        self.value = value
    
    def get_value(self):
        return self.value
    
    def __repr__(self):
        return "StandardString(%s)" % self.value


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
        



































