import time
import datetime
import  sqlite3
#a = datetime.datetime.now().strftime('%Y-%m-%d')


#a=(end - start).seconds

def get_conn():
    return sqlite3.connect("../carNumber.db")


def fetchAll():
   conn = get_conn()
   sql = "select * from number"
   cursor = conn.cursor()
   cursor.execute(sql)
   rows = cursor.fetchall()
   dic = {"reply":rows}
   return str(dic)

a = fetchAll()
def getTogether(a):
   s = ''
   data = eval(a)['reply']
   for i in range(len(data)):
      part = data[i][1]
      s = s + part + '\n'
   s = s + "There are still "+str(len(data))+" cars in the parking lot."
   return s
str = getTogether(a)
print(str)
def insert():
   c = counts()
   if c <100:
      conn = get_conn()
      sql = "insert into number values (?,?)"
      cursor = conn.cursor()
      cursor.execute(sql, (None, "test"))
      conn.commit()
      cursor.close()
      conn.close()
      print("saved.")
   else:
      print(0)

def counts():
   conn = get_conn()
   sql = "select count(id) from number"
   cursor = conn.cursor()
   cursor.execute(sql)
   rows = cursor.fetchall()

   conn.commit()
   cursor.close()
   conn.close()
   return rows[0][0]

def delete():
   conn = get_conn()
   sql = "delete from number where id =(?)"
   cursor = conn.cursor()
   a = 30
   cursor.execute(sql,(a,))
   conn.commit()
   cursor.close()
   conn.close()

def select():
   ip = "dddj"
   conn = get_conn()
   sql = "select * from number where number =(?)"
   cursor = conn.cursor()
   cursor.execute(sql,(ip,))
   rows = cursor.fetchall()
   if len(rows)==0:
      conn.commit()
      cursor.close()
      conn.close()
      return 0
   else:
      id = rows[0][1]
      conn.commit()
      cursor.close()
      conn.close()
      return id

