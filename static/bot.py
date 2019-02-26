import urllib.parse as up
import urllib.request as ur
from io import BytesIO
from PIL import Image
import json
import telepot
import base64
from telepot.loop import MessageLoop
import time
import threading
from threading import Thread
from queue import Queue

#发送请求函数
def sendReq(values,url):
    #url = 'http://127.0.0.1:5000/ '
    # values = {'req':'/start'}
    data = up.urlencode(values)
    data = data.encode('ascii')
    req = ur.Request(url, data)
    with ur.urlopen(req) as response:
        page = response.read()
        page = page.decode('utf-8')
    return page

def getNumbers():
    url = 'http://127.0.0.1:5000/empty '
    values=""
    res = sendReq(values, url)
    print(res)
    return res

def select():
    url = 'http://127.0.0.1:5000/select'
    values = ""
    res = sendReq(values, url)
    print(res)
    return res

def getTogether(a):
   s = ''
   data = eval(a)['reply']
   for i in range(len(data)):
      part = data[i][1]
      s = s + part + '\n'
   s = s + "There are still "+str(len(data))+" cars in the parking lot."
   return s

#接受图片函数
def receive_thread(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type == "text":
        if msg['text'] == "/getnumbers":
            num=getNumbers()
            bot.sendMessage(chat_id, "There are still "+num+" places in this parking lot.")
        elif msg['text'] == "/left":
            data = select()
            send = getTogether(data)
            bot.sendMessage(chat_id, send)
        else:
            print("type error")
            bot.sendMessage(chat_id, "Sorry, I just wanna a photo.")
    elif content_type == "photo":
        bot.download_file(msg['photo'][-1]['file_id'], 'image.png')
        image = Image.open("image.png")
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        encoded_img = base64.b64encode(buffered.getvalue())
        data = {'image': encoded_img.decode("utf-8")}
        data = json.dumps(data)
        next = {"data":data,"chat_id":chat_id}
        queue1.put(next)
        #bot.sendMessage(chat_id, res)
    else:
        print("type error")
        bot.sendMessage(chat_id, "Sorry, I just wanna a photo.")

#把图片发给sever
def send2Sever():
    while True:
        while not queue1.empty():
            last = queue1.get()
            image = last['data']
            chat_id = last['chat_id']
            value ={"name":image}
            url = 'http://127.0.0.1:5000/receive'
            res = eval(sendReq(value,url))
            next = {"result":res['rec'],"chat_id":chat_id,"status":res['status']}
            queue2.put(next)

#把回复发给users
def send2users():
    while True:
        while not queue2.empty():
            res = queue2.get()
            if res['status']==1:
                send = res['result']+" In."
                chat_id = res['chat_id']
                print(send)
                bot.sendMessage(chat_id, send)
            elif res['status']==-1:
                send = res['result'] + " Out."
                chat_id = res['chat_id']
                print(send)
                bot.sendMessage(chat_id, send)
            elif res['status']==0:
                send="The parking lot has already full."
                print(send)
                bot.sendMessage(chat_id, send)
#机器人
if __name__ == "__main__":
    queue1=Queue()
    queue2=Queue()
    bot = telepot.Bot('620336112:AAHlqfRRVrYY6VwN9RPrpFWiD9ZuSClEvvo')
    MessageLoop(bot,receive_thread).run_as_thread()
    threading.Thread(target=send2Sever,daemon=True).start()
    threading.Thread(target=send2users,daemon=True).start()
    for t in threading.enumerate():
        if t != threading.main_thread():
            t.join()