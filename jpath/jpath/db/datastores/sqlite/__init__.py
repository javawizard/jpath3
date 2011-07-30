
from jpath.db.store import DataStore
import sqlite3
from jpath.db.datastores.sqlite import tables, data as sd, update as u
from jpath.db.datastores.sqlite.types import *
import weakref

class SQLiteDataStore(DataStore):
    def __init__(self, file):
        self.database = sqlite3.connect(file)
        for statement in tables.initialize_statements:
            self.database.execute(statement)
        self.database.commit()
        existing_object_count = self.database.execute("select count(id) from objects").fetchone()[0]
        if existing_object_count == 0: # No objects, so we need to create the
            # root object. The id will be auto-generated for us.
            self.database.execute("insert into objects () values ()")
            self.database.commit()
        self.root = sd.SQLiteObject(self, 1, None, None)
        # Maps (type, value_id) to instances of SQLiteItem
        self.value_cache = weakref.WeakValueDictionary()
        # Maps (object_id, key) to instances of SQLitePair
        self.pair_cache = weakref.WeakValueDictionary()
    
    def get_root(self):
        return self.root
    
    def get_item(self, type, id, requester_type, requester_id):
        cache_key = (type, id)
        result = self.value_cache.get(cache_key, None)
        if result:
            return result
        result = self.get_uncached_item(type, id, requester_type, requester_id)
        self.value_cache[cache_key] = result
        return result
    
    def get_uncached_item(self, type, id, requester_type, requester_id):
        ItemClass = sd.types_to_classes[type]
        return ItemClass(self, id, requester_type, requester_id)
    
    def get_pair(self, object_id, key, value_type, value_id):
        cache_key = (object_id, key, value_type, value_id) # Not sure how many
        # of these are needed; technically it should only be object_id and
        # key, but I'm keeping the others for now
        result = self.pair_cache.get(cache_key, None)
        if result:
            return result
        result = self.get_uncached_pair(object_id, key, value_type, value_id)
        self.pair_cache[cache_key] = result
        return result
    
    def get_uncached_pair(self, object_id, key, value_type, value_id):
        return sd.SQLitePair(self, object_id, key, value_type, value_id)
    
    def apply_updates(self, updates):
        u.run_updates(self, updates)
    
    def commit(self):
        self.database.commit()
    
    def close(self):
        self.database.close()


def connect_to_name(name):
    return SQLiteDataStore(name)













