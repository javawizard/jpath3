
from abc import ABCMeta as ABC, abstractmethod as abstract

class Connection(object):
    __metaclass__ = ABC
    
    @abstract
    def call(self, module, function, *args): pass
    
    @abstract
    def run_module(self, module, update, vars={}): pass
    
    @abstract
    def run_query(self, query, update, vars={}): pass
