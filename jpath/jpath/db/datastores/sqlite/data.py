
from jpath.query import data as d
from jpath.db.datastore.sqlite.types import *

class SQLiteItem(object):
    @property
    def db(self):
        return self.datastore.database


class SQLiteNull(SQLiteItem, d.Null):
    def __init__(self, datastore, id):
        self.datastore = datastore
        self.id = id


class SQLiteBoolean(SQLiteItem, d.Boolean):
    def __init__(self, datastore, id):
        self.datastore = datastore
        self.id = id
        self.value = None
    
    def get_value(self):
        if self.value is not None:
            return self.value
        self.value = self.db.execute("select value from booleans where id = ?", (self.id,)).fetchone()[0]
        return self.value


class SQLiteNumber(SQLiteItem, d.Number):
    def __init__(self, datastore, id):
        self.datastore = datastore
        self.id = id
        self.value = None
    
    def get_as_float(self):
        return float(self._get_value())
    
    def get_as_int(self):
        return int(self._get_value())
    
    def _get_value(self):
        if self.value is not None:
            return self.value
        self.value = self.db.execute("select value from numbers where id = ?", (self.id,)).fetchone()[0]
        return self.value


class SQLiteString(SQLiteItem, d.Number):
    def __init__(self, datastore, id):
        self.datastore = datastore
        self.id = id
        self.value = None
    
    def get_value(self):
        if self.value is not None:
            return self.value
        self.value = self.db.execute("select value from strings where id = ?", (self.id,)).fetchone()[0]
        return self.value


class SQLitePair(SQLiteItem, d.Pair):
    def __init__(self, datastore, object_id, key, value_type, value_id):
        self.datastore = datastore
        self.object_id = object_id
        self.key = key
        self.key_string = SQLiteKeyString(datastore, object_id, key)
        self.value_type = value_type
        self.value_id = value_id
    
    def get_key(self):
        return self.key_string
    
    def get_value(self):
        return self.datastore.get_item(self.value_type, self.value_id)


class SQLiteKeyString(SQLiteItem, d.String):
    def __init__(self, datastore, object_id, key):
        self.datastore = datastore
        self.object_id = object_id
        self.key = key
    
    def get_value(self):
        return self.key


class SQLiteObject(SQLiteItem, d.Object):
    def __init__(self, datastore, id):
        self.datastore = datastore
        self.id = id
    
    def get_value(self, key):
        pass
    
    def get_pair(self, key):
        pass
    
    def get_values(self):
        pass
    
    def get_pairs(self):
        pass
    
    def get_size(self):
        pass


class SQLiteList(SQLiteItem, d.List):
    pass






































