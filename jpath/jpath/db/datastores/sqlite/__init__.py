
from jpath.db.store import DataStore
import sqlite3
from jpath.db.datastores.sqlite import tables

class SQLiteDataStore(DataStore):
    def __init__(self, file):
        self.database = sqlite3.connect(file)
        for statement in tables.create_statements:
            self.database.execute(statement)
        self.database.commit()
    
    def get_root(self):
        # FIXME: implement this
        pass


def connect_to_name(name):
    return SQLiteDataStore(name)
