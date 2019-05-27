#create db tables and load csv files
import csv
import codecs
import sqlite3
import pprint

table_list = ['nodes', 'nodes_tags', 'ways', 'ways_tags', 'ways_nodes']

con = sqlite3.connect("safety_harbor.db")
cur = con.cursor()

#drop tables if they exists so we do not insert repeat data
for tablename in table_list:
    stmt = "DROP TABLE IF EXISTS " + tablename
    cur.execute(stmt)
    con.commit()

# create nodes table
cur.execute("CREATE TABLE IF NOT EXISTS nodes (id, lat, lon, user, uid, version, changeset, timestamp);")

# load table
with codecs.open('nodes.csv', encoding='utf-8-sig') as fin:
    dr = csv.DictReader(fin)
    pprint.pprint(dr.fieldnames)
    to_db = [(i['id'], i['lat'], i['lon'], i['user'], i['uid'], i['version'], i['changeset'], i['timestamp']) for i in dr]

cur.executemany("INSERT INTO nodes (id, lat, lon, user, uid, version, changeset, timestamp) \
                VALUES (?, ?, ?, ?, ?, ?, ?, ?);", to_db)


# create nodes_tags table
cur.execute("CREATE TABLE IF NOT EXISTS nodes_tags (id, key, value, type);")

# load table
with codecs.open('nodes_tags.csv', encoding='utf-8-sig') as fin:
    dr = csv.DictReader(fin)
    pprint.pprint(dr.fieldnames)
    to_db = [(i['id'], i['key'], i['value'], i['type']) for i in dr]

cur.executemany("INSERT INTO nodes_tags (id, key, value, type) VALUES (?, ?, ?, ?);", to_db)


# create ways table
cur.execute("CREATE TABLE IF NOT EXISTS ways (id, user, uid, version, changeset, timestamp);")

# load table
with codecs.open('ways.csv', encoding='utf-8-sig') as fin:
    dr = csv.DictReader(fin)
    pprint.pprint(dr.fieldnames)
    to_db = [(i['id'], i['user'], i['uid'], i['version'], i['changeset'], i['timestamp']) for i in dr]

cur.executemany("INSERT INTO ways (id, user, uid, version, changeset, timestamp) VALUES (?, ?, ?, ?, ?, ?);", to_db)


# create ways_nodes table
cur.execute("CREATE TABLE IF NOT EXISTS ways_nodes (id, node_id, position);")

# load table
with codecs.open('ways_nodes.csv', encoding='utf-8-sig') as fin:
    dr = csv.DictReader(fin)
    pprint.pprint(dr.fieldnames)
    to_db = [(i['id'], i['node_id'], i['position']) for i in dr]

cur.executemany("INSERT INTO ways_nodes (id, node_id, position) VALUES (?, ?, ?);", to_db)

# create ways_tags table
cur.execute("CREATE TABLE IF NOT EXISTS ways_tags (id, key, value, type);")

# load table
with codecs.open('ways_tags.csv', encoding='utf-8-sig') as fin:
    dr = csv.DictReader(fin)
    pprint.pprint(dr.fieldnames)
    to_db = [(i['id'], i['key'], i['value'], i['type']) for i in dr]

cur.executemany("INSERT INTO ways_tags (id, key, value, type) VALUES (?, ?, ?, ?);", to_db)

con.commit()

for tablename in table_list:
    stmt = 'SELECT COUNT(*) FROM ' + tablename
    cur.execute(stmt)
    rows = cur.fetchall()
    print("--------------------------------------------------------------")
    print(tablename + " Row Count:", rows)


con.close()
