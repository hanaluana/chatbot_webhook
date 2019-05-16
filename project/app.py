from flask import Flask, request, render_template
import os
import requests
from pprint import pprint as pp
import random
from bs4 import BeautifulSoup
import urllib

app = Flask(__name__)

# 텔레그램이 우리에게 알림을 줄 때 사용할 route
# 만약 특정 유저가 우리 봇으로 메시지를 보내게 되면,
# 텔레그램이 우리에게 알림을 보내온다. (json 형태로)

# 그 전에, 웹훅 설정해준다. (set webhook)
# 웹훅이란: 텔레그램에게 알리미를 해달라고 하는 것

token = "782982995:AAH9pktG9vNPLHgo3TrYW5ZMoGyUjNJ1xog"
base_url = "https://api.hphk.io/telegram"
my_url = "https://facerecognition-hzzle.c9users.io"
naver_id = '1elzfrgpIhDHOhtTSZEi'
naver_secret = 'Ey9goMTgiW'
songkick_key = 'XFK6hX8iZ4LjPg6l'

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
    #pp(doc)
    chat_id = doc['message']['chat']['id']
    img = False
    print(token)
    
    if doc.get('message').get('photo') is not None:
        img = True
    
    if img:
        file_id = doc.get('message').get('photo')[-1].get('file_id')
        file = requests.get("{}/bot{}/getFile?file_id={}".format(base_url, token, file_id))
        file_url = "{}/file/bot{}/{}".format(base_url, token, file.json().get('result').get('file_path'))
        
        # 네이버로 요청
        requests.get('{}/bot{}/sendMessage?chat_id={}&text={}'.format(base_url, token, chat_id, '분석 중입니다'))

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
            # print(clova_res.json().get('faces'))
            reply = "{}: {:.2f}".format(clova_res.json().get('faces')[0].get('celebrity').get('value'), float(clova_res.json().get('faces')[0].get('celebrity').get('confidence'))*100)
        else:
            reply = "인식된 사람이 없습니다."
        print(reply)
    else:
        if '안녕' in doc['message']['text']: 
            reply = '좋아하는 가수를 입력하세요'
        elif 'hello' in doc['message']['text'].lower():
            reply = 'Tell us your favourite singer'
        else:
            artist_name = doc['message']['text'].replace(" ","+")
            artist_res = requests.get('https://www.songkick.com/search?utf8=✓&type=initial&query='+artist_name).text
            artist_doc = BeautifulSoup(artist_res, 'html.parser')
            # print(artist_doc)
            if not artist_doc.find('p',{'class': 'summary'}):
                reply="가수를 찾을 수가 없습니다"
            else:
                artist_url = artist_doc.find('p',{'class': 'summary'}).find('a')['href']
                artist_id = artist_url.split('/')[2].split('-')[0]
                artist_info = requests.get('https://api.songkick.com/api/3.0/artists/{}/calendar.json?apikey={}'.format(artist_id, songkick_key))
                #reply = '연예인 사진을 올려주세요!'
                #artist_info2 = BeautifulSoup(artist_info, 'html.parser')
                events = artist_info.json().get('resultsPage').get('results').get('event')
                print('https://api.songkick.com/api/3.0/artists/{}/calendar.json?apikey={}'.format(artist_id, songkick_key))
                if not events:
                    reply = "가수의 다가오는 공연이 없습니다"
                else:
                    if len(events)>15:
                        events=events[:15]
                    reply = artist_name+"의 공연 정보 입니다.\n\n"
                    i=1
                    # print("length: {}".format(len(events)))
                    for e in events:
                        s = ''
                        s = s+str(i)+'. '+e.get('displayName')+'\n'
                        s = s+"날짜: "+e.get('start').get('date')+'\n'
                        if e.get('start').get('time'):
                            s = s+"시간: "+e.get('start').get('time')+'\n'
                        s = s+"도시: "+e.get('location').get('city')+'\n'
                        s = s+"장소: "+e.get('venue').get('displayName')+'\n'
                        s = s+"-----------------------------\n"
                        reply+=s
                        i+=1

    requests.get('{}/bot{}/sendMessage?chat_id={}&text={}'.format(base_url, token, chat_id, reply))
    
    return '', 200

@app.route('/setwebhook')
def setwebhook():
    url = "{}/bot{}/setWebhook?url={}/{}".format(base_url, token, my_url, token)
    res = requests.get(url)
    return '{}'.format(res) , 200


#@app.route('')
