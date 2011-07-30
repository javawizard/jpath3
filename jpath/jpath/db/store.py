
from abc import ABCMeta as ABC, abstractmethod as abstract

class DataStore(object):
    __metaclass__ = ABC
    
    @abstract
    def get_root(self): pass
    
    @abstract
    def apply_updates(self, updates): pass
    
    @abstract
    def commit(self): pass
    
    @abstract
    def rollback(self): pass
    
    @abstract
    def close(self): pass