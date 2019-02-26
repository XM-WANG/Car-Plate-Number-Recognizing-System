from flask import Flask,jsonify,request
from hyperlpr import *
import cv2
import json
import base64
import sqlite3
app = Flask(__name__)

#连接到sqlite
def get_conn():
    return sqlite3.connect("carNumber.db")

#插入车牌号
def insert(num):
    c = counts()
    id = select(num)
    if id == 0:
        if c < 100:
            conn = get_conn()
            sql = "insert into number values (?,?)"
            cursor = conn.cursor()
            cursor.execute(sql, (None, num))
            conn.commit()
            cursor.close()
            conn.close()
            print("saved.")
            return 1
        else:
            print("Full.")
            return 0
    else:
        delete(id)
        print("Car Out.")
        return -1

#删除一条数据
def delete(foo):
   conn = get_conn()
   sql = "delete from number where id =(?)"
   cursor = conn.cursor()
   cursor.execute(sql,(foo,))
   conn.commit()
   cursor.close()
   conn.close()


#查一条数据
def select(num):
   conn = get_conn()
   sql = "select * from number where number =(?)"
   cursor = conn.cursor()
   cursor.execute(sql,(num,))
   rows = cursor.fetchall()
   if len(rows)==0:
      conn.commit()
      cursor.close()
      conn.close()
      return 0
   else:
      id = rows[0][0]
      conn.commit()
      cursor.close()
      conn.close()
      return id


#返回数据库内条数(返回车库内数目）
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

@app.route('/receive',methods=['POST'])
def saveImage():
    data = eval(request.form.get('name'))
    image = base64.b64decode(data['image'])
    with open('image.jpg', 'wb') as f:
        f.write(image)
    print("ok")
    image = cv2.imread("image.jpg")
    res = HyperLPR_PlateRecogntion(image)
    print(res)
    if res==[]:
        return "Sorry, I cannot find the number plate in the picture."
    else:
        db = insert(res[0][0])
        print(db)
        #print(type(res[0][0]))
        bk = {"status":db,"rec":res[0][0]}
        return str(bk)

@app.route('/select',methods=['POST'])
def fetchAll():
   conn = get_conn()
   sql = "select * from number"
   cursor = conn.cursor()
   cursor.execute(sql)
   rows = cursor.fetchall()
   dic = {"reply":rows}
   return str(dic)

@app.route('/empty',methods=['POST'])
def getEmpty():
    c = counts()
    res = 100 - c
    return str(res)

@app.route('/',methods=['POST'])
def loadCommmands():
   return ""


if __name__ == '__main__':
    app.run(debug=True)
