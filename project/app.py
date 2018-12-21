from flask import Flask, request, render_template
import os
import requests
from pprint import pprint as pp
import random

app = Flask(__name__)

# 텔레그램이 우리에게 알림을 줄 때 사용할 route
# 만약 특정 유저가 우리 봇으로 메시지를 보내게 되면,
# 텔레그램이 우리에게 알림을 보내온다. (json 형태로)

# 그 전에, 웹훅 설정해준다. (set webhook)
# 웹훅이란: 텔레그램에게 알리미를 해달라고 하는 것

token = os.getenv('TELEGRAM_TOKEN')
base_url = "https://api.hphk.io/telegram"
my_url = "https://facerecognition-hzzle.c9users.io"
naver_id = 'YeCKsdLSZCDitBhXvKH2'
naver_secret = 'aS4lYl4HpK'

# post 방식으로 우리한테 옴
# @app.route('/{}'.format(token), methods=['GET','POST'])
# def telegram():
#     doc = request.get_json()
#     pp(doc)
#     msg= '닥쳐'
    # chat_id = doc['message']['chat']['id']
    # text = doc['message'].get('text')  
    # if text in ('로또', 'lotto'):
    #     reply = str(random.sample(range(1,46),6))
    # elif msg == '비트코인':
    #     pass
    # elif msg == '이더리움':
    #     pass
    # else:
    #     reply=text
    
#     url = "{}/bot{}/sendMessage?chat_id={}&text={}".format(base_url,token,chat_id,reply)
#     requests.get(url)
    
#     return '', 200

@app.route("/{}".format(token), methods=['POST'])
def telegram():
    doc = request.get_json()
    pp(doc)
    chat_id = doc['message']['chat']['id']
    img = False
    
    if doc.get('message').get('photo') is not None:
        img = True
    
    if img:
        file_id = doc.get('message').get('photo')[-1].get('file_id')
        file = requests.get("{}/bot{}/getFile?file_id={}".format(base_url, token, file_id))
        file_url = "{}/file/bot{}/{}".format(base_url, token, file.json().get('result').get('file_path'))
        
        # 네이버로 요청
        res = requests.get(file_url, stream=True)
        clova_res = requests.post('https://openapi.naver.com/v1/vision/celebrity', # 클로바한테 post request를 보냄
            headers={
                'X-Naver-Client-Id':naver_id,
                'X-Naver-Client-Secret':naver_secret
            },
            files={
                'image':res.raw.read()
            })
        if clova_res.json().get('info').get('faceCount'):
            print(clova_res.json().get('faces'))
            reply = "{}: {}".format(clova_res.json().get('faces')[0].get('celebrity').get('value'), float(clova_res.json().get('faces')[0].get('celebrity').get('confidence'))*100 )
        else:
            reply = "인식된 사람이 없습니다."
            
    else:
        reply = doc['message']['text']
        
        
    requests.get('{}/bot{}/sendMessage?chat_id={}&text={}'.format(base_url, token, chat_id, reply))
    
    return '', 200

@app.route('/setwebhook')
def setwebhook():
    url = "{}/bot{}/setWebhook?url={}/{}".format(base_url, token, my_url, token)
    res = requests.get(url)
    return '{}'.format(res) , 200


#@app.route('')
