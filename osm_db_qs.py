import sqlite3

con = sqlite3.connect("safety_harbor.db")
cur = con.cursor()

#table columns
#nodes (id, lat, lon, user, uid, version, changeset, timestamp)
#ways  (id, user, uid, version, changeset, timestamp)
#nodes_tags (id, key, value, type)
#ways_tags  (id, key, value, type)
#ways_nodes (id, node_id, position)

table_list = ['nodes', 'nodes_tags', 'ways', 'ways_tags', 'ways_nodes']


amenityQ = 'SELECT value, COUNT(*) as num FROM nodes_tags WHERE  key="amenity" GROUP BY value ORDER BY num DESC LIMIT 1'

uniqueUsrQ = 'SELECT COUNT(distinct(uid)) FROM (SELECT uid FROM nodes UNION ALL SELECT uid FROM ways)'

topConQ = 'SELECT e.user, COUNT(*) as num FROM (SELECT user FROM nodes  UNION ALL SELECT user FROM ways) e GROUP BY e.user ORDER BY num DESC  LIMIT 1'

religQ = 'SELECT nodes_tags.value, COUNT(*) as num FROM nodes_tags JOIN (SELECT DISTINCT(id) FROM nodes_tags WHERE value="place_of_worship") i ON nodes_tags.id=i.id WHERE nodes_tags.key="religion" GROUP BY nodes_tags.value ORDER BY num DESC LIMIT 1'

def table_counts():
    for tablename in table_list:
        query = 'SELECT COUNT(*) FROM ' + tablename
        cur.execute(query)
        rows = cur.fetchall()
        print(tablename, " total rows:", rows)

def run_query(query):
    for row in cur.execute(query):
        return row



if __name__ == '__main__':
    table_counts()
    print("Number of unique users: ", run_query(uniqueUsrQ))
    print("Top contributing user : ", run_query(topConQ))
    print("Biggest religion      : ", run_query(religQ))
    print("Popular amenity       : ", run_query(amenityQ))
