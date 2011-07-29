
headers = "id integer primary key autoincrement"

prefix = "create table if not exists"

create_objects = prefix + "objects (%s)" % headers
create_lists = prefix + "lists (%s)" % headers
create_strings = prefix + "strings (%s, value text)" % headers
create_numbers = prefix + "numbers (%s, value real)" % headers
create_booleans = prefix + "booleans (%s, value boolean)" % headers
create_nulls = prefix + "nulls (%s)" % headers

create_listvalues = prefix + """listvalues (
id integer,
position integer,
type int8,
value integer
)"""

create_objectentries = prefix + """objectentries (
id integer,
key text,
type int8,
value integer
)"""

set_auto_vacuum = "pragma auto_vacuum = full"

initialize_statements = [set_auto_vacuum, create_objects, create_lists, create_strings,
        create_numbers, create_booleans, create_nulls,
        create_listvalues, create_objectentries]














