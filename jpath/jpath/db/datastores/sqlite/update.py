
from jpath.db.datastores.sqlite import data as sd
from jpath.db.datastores.sqlite.types import *
from jpath.query import data as d, exceptions as e

def run_updates(datastore, updates):
    for update in updates:
        run_single_update(datastore, update)


def run_single_update(datastore, update):
    if not isinstance(update, d.Update):
        raise e.TypeException("Updates must be instances of jpath.query.data.Update,"
                " not " + str(type(update)))
    # So... What do we do here? Well... We probably need to have a separate
    # branch for each type. Let's do that.
    if isinstance(update, d.Insert):
        run_insert(datastore, update)
    elif isinstance(update, d.Delete):
        run_delete(datastore, update)
    elif isinstance(update, d.Replace):
        run_replace(datastore, update)
    elif isinstance(update, d.Merge):
        run_merge(datastore, update)
    else:
        raise e.TypeException("Unknown update type " + str(type(update)))


def run_insert(datastore, insert):
    value = insert.get_value()
    target = insert.get_reference()
    if not isinstance(target, sd.SQLiteItem):
        raise e.TypeException("Can't insert into or next to any value that's "
                "not a SQLite item, and you just tried to insert into or "
                "next to a value of type " + str(type(target)))
    position = insert.get_position()
    if position in ("before", "after"):
        raise e.OtherException("Inserting before/after another value isn't "
                "supported yet. Try inserting at a specific position.")
    if isinstance(target, sd.SQLiteList):
        pass
    elif isinstance(target, sd.SQLiteObject):
        
    else:
        raise e.TypeException("Only SQLiteList and SQLiteObject values can "
                "be the target of an insert statement, not " + str(type(insert)))


def run_delete(datastore, delete):
    pass


def run_replace(datastore, replace):
    pass


def run_merge(datastore, merge):
    pass







































