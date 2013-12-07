import MySQLdb as m

db = m.connect(host="localhost",user="root",db="sandbox")

#port: 3306
#connection_name:test

cursor = db.cursor()



# try:
#    x.execute("""INSERT INTO first_python_insert VALUES (%s,%s)""",(2,'this is my second python insert yall!'))
#    conn.commit()
# except:
#    conn.rollback()


# execute SQL select statement
genre_m_id = '/m/06953q'


g_sql = "select genre_id from genres where m_id  = '" + str(genre_m_id) + "'"

cursor.execute(g_sql)

# commit your changes
db.commit()

# get the number of rows in the resultset
numrows = int(cursor.rowcount)

print numrows

# get and display one row at a time.
for x in range(0,numrows):
    row = cursor.fetchone()
    genre_id = row[0]
    print genre_id


# conn.close()


