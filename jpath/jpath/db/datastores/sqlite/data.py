
from jpath.query import data as d
from jpath.db.datastores.sqlite.types import *

# Where parents are passed as parameter to values, the parent should be a
# tuple (type, id) representing the parent.

class SQLiteItem(object):
    @property
    def db(self):
        return self.datastore.database


class SQLiteNull(SQLiteItem, d.Null):
    sqlite_type = NULL
    
    def __init__(self, datastore, id, parent_type, parent_id):
        self.datastore = datastore
        self.id = id
        self.parent_type = parent_type
        self.parent_id = parent_id


class SQLiteBoolean(SQLiteItem, d.Boolean):
    sqlite_type = BOOLEAN
    
    def __init__(self, datastore, id, parent_type, parent_id):
        self.datastore = datastore
        self.id = id
        self.parent_type = parent_type
        self.parent_id = parent_id
        self.value = None
    
    def get_value(self):
        if self.value is not None:
            return self.value
        self.value = self.db.execute("select value from booleans where id = ?", (self.id,)).fetchone()[0]
        return self.value


class SQLiteNumber(SQLiteItem, d.Number):
    sqlite_type = NUMBER
    
    def __init__(self, datastore, id, parent_type, parent_id):
        self.datastore = datastore
        self.id = id
        self.parent_type = parent_type
        self.parent_id = parent_id
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
    sqlite_type = STRING
    
    def __init__(self, datastore, id, parent_type, parent_id):
        self.datastore = datastore
        self.id = id
        self.parent_type = parent_type
        self.parent_id = parent_id
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
        return self.datastore.get_item(self.value_type, self.value_id, OBJECT, self.object_id)


class SQLiteKeyString(SQLiteItem, d.String):
    def __init__(self, datastore, object_id, key):
        self.datastore = datastore
        self.object_id = object_id
        self.key = key
    
    def get_value(self):
        return self.key


class SQLiteObject(SQLiteItem, d.Object):
    sqlite_type = OBJECT
    
    def __init__(self, datastore, id, parent_type, parent_id):
        self.datastore = datastore
        self.id = id
        self.parent_type = parent_type
        self.parent_id = parent_id
        # For now, we're precomputing the size. In the future we might want to
        # compute it on-the-fly if we ever decide to allow these values to
        # properly respond to changes in the database.
        self.size = self.db.execute("select count(key) from objectentries where id = ?", (self.id,)).fetchone()[0]
    
    def get_value(self, key):
        result = self.db.execute("select type, id from objectentries where id = ? and key = ?", (self.id, key)).fetchone()
        if not result: # No such key
            return None
        return self.datastore.get_item(result[0], result[1], OBJECT, self.id)
    
    def get_pair(self, key):
        result = self.db.execute("select type, id from objectentries where id = ? and key = ?", (self.id, key)).fetchone()
        if not result: # No such key
            return None
        return self.datastore.get_pair(self.id, key, result[0], result[1])
    
    def get_values(self):
        return SQLiteObjectValueSequence(self)
    
    def get_pairs(self):
        return SQLiteObjectPairSequence(self)
    
    def get_size(self):
        return self.size


class SQLiteObjectValueSequence(d.Sequence):
    def __init__(self, object, size):
        self.object = object
    
    def get_size(self):
        return self.object.size
    
    def get_value(self, index):
        type, id = self.object.db.execute(
                "select type, value from objectentries where id = ? order by key asc limit 1 offset ?", 
                (self.object.id, index)).fetchone()
        return self.object.datastore.get_item(type, id)


class SQLiteObjectPairSequence(d.Sequence):
    def __init__(self, object):
        self.object = object
    
    def get_size(self):
        return self.object.size
    
    def get_value(self, index):
        key, type, id = self.object.db.execute(
                "select key, type, value from objectentries where id = ? order by key asc limit 1 offset ?", 
                (self.object.id, index)).fetchone()
        return self.object.datastore.get_pair(self.object.id, key, type, id)


class SQLiteList(SQLiteItem, d.List):
    sqlite_type = LIST


types_to_classes = {
        NULL: SQLiteNull,
        BOOLEAN: SQLiteBoolean,
        NUMBER: SQLiteNumber,
        STRING: SQLiteString,
        LIST: SQLiteList,
        OBJECT: SQLiteObject
    }






































