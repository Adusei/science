import MySQLdb as m

conn = m.connect(host="localhost",user="root",db="sandbox")

#port: 3306
#connection_name:test

x = conn.cursor()

try:
   x.execute("""INSERT INTO first_python_insert VALUES (%s,%s)""",(2,'this is my second python insert yall!'))
   conn.commit()
except:
   conn.rollback()



conn.close()