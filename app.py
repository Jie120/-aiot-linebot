from __future__ import unicode_literals
from flask import Flask, request, abort, render_template
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from string import ascii_letters
import requests
import json
import configparser
import os
from urllib import parse
from google.cloud import vision
import random
import string
import pymysql
app = Flask(__name__, static_url_path='/static')
UPLOAD_FOLDER = 'static'
ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg', 'gif'])


config = configparser.ConfigParser()
config.read('config.ini')

line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))
handler = WebhookHandler(config.get('line-bot', 'channel_secret'))
my_line_id = config.get('line-bot', 'my_line_id')
end_point = config.get('line-bot', 'end_point')
my_phone = config.get('line-bot', 'my_phone')
db = config.get('line-bot', 'db')
user = config.get('line-bot', 'user')
password = config.get('line-bot',"password")
host = config.get('line-bot',"host")
port = int(config.get('line-bot', "port"))

HEADER = {
    'Content-type': 'application/json',
    'Authorization': F'Bearer {config.get("line-bot", "channel_access_token")}'
}

con = pymysql.connect(db=db,user=user,password=password,host=host,port=port,autocommit=True)
cur = con.cursor()













@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == 'GET':
        return 'ok'
    body = request.json
    events = body["events"]
    print(body)
    if "replyToken" in events[0]:
        payload = dict()
        replyToken = events[0]["replyToken"]
        payload["replyToken"] = replyToken
        if events[0]["type"] == "message":
            if events[0]["message"]["type"] == "text":
                text = events[0]["message"]["text"]

                # if text == "網路爬蟲":
                #     payload["messages"] = [getNamedep1()]
                # elif text == "MySQL資料庫":
                #     payload["messages"] = [getNamedep1_2()]
                # elif text == "資料分析和模型訓練":
                #     payload["messages"] = [getNamedep2()]
                # elif text == "LineBOT":
                #     payload["messages"] = [getNamedep3()]
                # elif text == "網頁架設":
                #     payload["messages"] = [getNamedep4()]
                # elif text == "AIOT整合":
                #     payload["messages"] = [getNamedep4_1()]
                # if text == "即時影像觀看":
                #     payload["messages"] = [getUri()]
                if text == "使用教學":
                    payload["messages"] = [getMRTVideoMessage()]
                elif text == "貨物辨識":
                    payload["messages"] = [
                            {
                                "type":"text",
                                "text":"發送欲辨識編號圖片",
                                "quickReply":{
                                    "items": [
                                        {
                                            "type": "action",
                                            "action": {
                                                "type": "cameraRoll",
                                                "label": "開啟圖庫"
                                            }
                                        },
                                        {
                                            "type": "action",
                                            "action": {
                                                "type": "camera",
                                                "label": "開啟相機"
                                            }
                                        }
                                    ]
                                }
                            }
                        ]
                elif text == "工作人員聯繫":
                    payload["messages"] = [
                            {
                                "type": "template",
                                "altText": "this is a carousel template",
                                "template": {
                                "type": "carousel",
                                "columns": [
                                    {
                                        "thumbnailImageUrl": F"{end_point}/static/boy.jpg",
                                        "imageBackgroundColor": "#FFFFFF",
                                        "title": "陳偉傑",
                                        "text": "Linebot相關",
                                        "defaultAction": {
                                            "type": "uri",
                                            "label": "View detail",
                                            "uri":  F"{end_point}/page/123"
                                                            },
                                        "actions": [
                                            {
                                                "type": "uri",
                                                "label": "連絡電話",
                                                "uri": "tel:0912345678"
                                            },
                                            # {
                                            #     "type": "postback",
                                            #     "label": "錯誤回報",
                                            #     "data": "action=add&itemid=111",
                                            #     "displayText": "回報",
                                            #     "inputOption": "openKeyboard",
                                            #     "fillInText": "Name: \nPhone: \nBirthday: "
                                            # },
                                            {
                                                "type": "uri",
                                                "label": "個人資訊",
                                                "uri": "https://www.youtube.com/watch?v=kAnP9EEgLwU"
                                            }
                                                    ]
                                    },
                                    {
                                        "thumbnailImageUrl": F"{end_point}/static/girl.jpg",
                                        "imageBackgroundColor": "#FFFFFF",
                                        "title": "陳彥秀",
                                        "text": "爬蟲相關",
                                        "defaultAction": {
                                            "type": "uri",
                                            "label": "View detail",
                                            "uri":  F"{end_point}/page/124"
                                                            },
                                        "actions": [
                                            {
                                                "type": "uri",
                                                "label": "連絡電話",
                                                "uri": "tel:0912345678"
                                            },
                                            # {
                                            #     "type": "postback",
                                            #     "label": "錯誤回報",
                                            #     "data": "action=add&itemid=111",
                                            #     "displayText": "回報",
                                            #     "inputOption": "openKeyboard",
                                            #     "fillInText": "Name: \nPhone: \nBirthday: "
                                            # },
                                            {
                                                "type": "uri",
                                                "label": "個人資訊",
                                                "uri": "https://www.youtube.com/watch?v=kAnP9EEgLwU"
                                            }
                                                    ]
                                    },
                                    {
                                        "thumbnailImageUrl": F"{end_point}/static/girl.jpg",
                                        "imageBackgroundColor": "#FFFFFF",
                                        "title": "謝欣庭",
                                        "text": "資料庫相關",
                                        "defaultAction": {
                                            "type": "uri",
                                            "label": "View detail",
                                            "uri": F"{end_point}/page/125"
                                                            },
                                        "actions": [
                                            {
                                                "type": "uri",
                                                "label": "連絡電話",
                                                "uri": "tel:0912345678"
                                            },
                                            # {
                                            #     "type": "postback",
                                            #     "label": "錯誤回報",
                                            #     "data": "action=add&itemid=111",
                                            #     "displayText": "回報",
                                            #     "inputOption": "openKeyboard",
                                            #     "fillInText": "Name: \nPhone: \nBirthday: "
                                            # },
                                            {
                                                "type": "uri",
                                                "label": "個人資訊",
                                                "uri": "https://www.youtube.com/watch?v=kAnP9EEgLwU"
                                            }
                                                    ]
                                    },
                                    {
                                        "thumbnailImageUrl": F"{end_point}/static/666.jpg",
                                        "imageBackgroundColor": "#FFFFFF",
                                        "title": "李昇融",
                                        "text": "資料分析相關",
                                        "defaultAction": {
                                            "type": "uri",
                                            "label": "View detail",
                                            "uri": F"{end_point}/page/126"
                                                            },
                                        "actions": [
                                            {
                                                "type": "uri",
                                                "label": "連絡電話",
                                                "uri": "tel:0912345678"
                                            },
                                            # {
                                            #     "type": "postback",
                                            #     "label": "錯誤回報",
                                            #     "data": "action=add&itemid=111",
                                            #     # "displayText": "回報",
                                            #     "inputOption": "openKeyboard",
                                            #     "fillInText": "Name: \nPhone: \nBirthday: "
                                            # },
                                            {
                                                "type": "uri",
                                                "label": "個人資訊",
                                                "uri": "https://www.youtube.com/watch?v=kAnP9EEgLwU"
                                            }
                                                    ]
                                    },
                                    {
                                        "thumbnailImageUrl": F"{end_point}/static/boy.jpg",
                                        "imageBackgroundColor": "#FFFFFF",
                                        "title": "林奕全",
                                        "text": "硬體、辨識與網頁相關",
                                        "defaultAction": {
                                            "type": "uri",
                                            "label": "View detail",
                                            "uri": F"{end_point}/page/127"
                                        },
                                        "actions": [
                                            {
                                                "type": "uri",
                                                "label": "連絡電話",
                                                "uri": "tel:0912345678"
                                            },
                                            # {
                                            #     "type": "postback",
                                            #     "label": "錯誤回報",
                                            #     "data": "action=add&itemid=111",
                                            #     "displayText": "回報",
                                            #     "inputOption": "openKeyboard",
                                            #     "fillInText": "Name: \nPhone: \nBirthday: "
                                            # },
                                            {
                                                "type": "uri",
                                                "label": "個人資訊",
                                                "uri": "https://www.youtube.com/watch?v=kAnP9EEgLwU"
                                            }
                                        ]
                                    },
                                    {
                                        "thumbnailImageUrl": F"{end_point}/static/girl.jpg",
                                        "imageBackgroundColor": "#FFFFFF",
                                        "title": "范詩涵",
                                        "text": "硬體與辨識相關",
                                        "defaultAction": {
                                            "type": "uri",
                                            "label": "View detail",
                                            "uri": F"{end_point}/page/128"
                                        },
                                        "actions": [
                                            {
                                                "type": "uri",
                                                "label": "連絡電話",
                                                "uri": "tel:0912345678"
                                            },
                                            # {
                                            #     "type": "postback",
                                            #     "label": "錯誤回報",
                                            #     "data": "action=add&itemid=111",
                                            #     "displayText": "回報",
                                            #     "inputOption": "openKeyboard",
                                            #     "fillInText": "Name: \nPhone: \nBirthday: "
                                            # },
                                            {
                                                "type": "uri",
                                                "label": "個人資訊",
                                                "uri": "https://www.youtube.com/watch?v=kAnP9EEgLwU"
                                            }
                                        ]
                                    }
                                            ],
                                "imageAspectRatio": "rectangle",
                                "imageSize": "contain"
                            }
                        }
                    ]


                else:
                    payload["messages"] = [
                            {
                                "type": "text",
                                "text": text
                            }
                        ]

                replyMessage(payload)
            elif events[0]["message"]["type"] == "image":
                image_name = "".join(random.choice(string.ascii_letters+string.digits) for x in range(4))
                image_content = line_bot_api.get_message_content(events[0]["message"]["id"])
                image_name = image_name.upper() + ".jpg"
                path = "./static/pic/" + image_name
                with open(path, "wb") as fd:
                    for chunk in image_content.iter_content():
                        fd.write(chunk)                               ##322-329 功能是將圖片存在本地端資料夾
                #YOUR_SERVICE = 'yyyy120.json'          ##GCP雲端要註解掉 需要VISION服務對象的金耀
                YOUR_PIC = path
                #os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = YOUR_SERVICE    #GCP雲端要註解掉
                client = vision.ImageAnnotatorClient()
                with open(YOUR_PIC, 'rb') as image_file:
                    content = image_file.read()
                image = vision.Image(content=content)
                response = client.text_detection(image=image)
                for y in response.text_annotations:
                    print(type(y.description))  #330-339 vision gcp TeXT-detection 辨識功能
                    sku = str(y.description)     #以下就是進本地MYSQL資料庫用回傳的文字查詢商品
                    db_1 = pymysql.connect(db=db,user=user,password=password,host=host,port=port,autocommit=True)
                    cursor = db_1.cursor()
                    cursor.execute("SELECT * FROM AioT.product where sku = '" + str(sku) + "'")
                    data = cursor.fetchall()
                    if (data):
                        for tp in data:
                            p_n = str(tp[1])
                            c_n = str(tp[10])
                            payload["messages"] = [
                    {
                        "type": "text",
                        "text": "商品名稱:\n" + p_n + "\n商品分類:\n" + c_n
                    }
                ]
                    else:
                        payload["messages"] = [
                            {
                                "type": "text",
                                "text": "找不到商品"
                            }
                        ]


                replyMessage(payload)


    return 'OK'


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)

    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def pretty_echo(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text)
        )







@app.route("/sendTextMessageToMe", methods=['POST'])
def sendTextMessageToMe():
    pushMessage({})
    return 'OK'


# def getNamedep1():
#     message = dict()
#     message["type"] = "text"
#     message["text"] = "Name:陳彥秀\nTel:0912345678\nMessage:\tiuui8069@gmail.com"
#
#     return message
# def getNamedep1_2():
#     message = dict()
#     message["type"] = "text"
#     message["text"] = "Name:謝欣庭\nTel:0912345678\nMessage:\tsheila86.hsieh@gmail.com"
#     return message
#
# def getNamedep2():
#     message = dict()
#     message["type"] = "text"
#     message["text"] = "Name:李昇融\nTel:0912345678\nMessage:\tapple123116@gmail.com"
#     return message
#
# def getNamedep3():
#     message = dict()
#     message["type"] = "text"
#     message["text"] = "Name:陳偉傑\nTel:0912345678\nMessage:\tmissfly120@gmail.com"
#     return message
#
# def getNamedep4():
#     message = dict()
#     message["type"] = "text"
#     message["text"] = "Name:林奕全\nTel:0912345678\nMessage:\tfm06u4xup6@gmail.com"
#     return message
#
# def getNamedep4_1():
#     message = dict()
#     message["type"] = "text"
#     message["text"] = "Name:范詩涵\nTel:0912345678\nMessage:\tlouislianjapan666@gmail.com"
#     return message



# def getUri():
#     massage = dict()
#     message["type"] = "uri"
#     message["label"] = "即時影像觀看"
#     message["uri"] = "https://www.youtube.com/shorts/w3ROtvSzVc"
#
#     return massage


# def getCarouselMessage(data):
#     message = {
#       "type": "template",
#       "altText": "this is a image carousel template",
#       "template": {
#           "type": "image_carousel",
#           "columns": [
#               {
#                 "imageUrl": F"{end_point}/static/taipei_101.jpeg",
#                 "action": {
#                   "type": "postback",
#                   "label": "台北101",
#                   "data": json.dumps(data)
#                 }
#               },
#               {
#                 "imageUrl": F"{end_point}/static/taipei_1.jpeg",
#                 "action": {
#                   "type": "postback",
#                   "label": "台北101",
#                   "data": json.dumps(data)
#                 }
#               }
#           ]
#           }
#         }
#     return message


# def getLocationConfirmMessage(title, latitude, longitude):
#     data = {'title': title, 'latitude': latitude, 'longitude': longitude,
#             'action': 'get_near'}
#     message = {
#       "type": "template",
#       "altText": "this is a confirm template",
#       "template": {
#           "type": "confirm",
#           "text": f"確認是否搜尋 {title} 附近地點？",
#           "actions": [
#               {
#                  "type": "postback",
#                "label": "是",
#                "data": json.dumps(data),
#                },
#               {
#                 "type": "message",
#                 "label": "否",
#                 "text": "否"
#               }
#           ]
#       }
#     }
#     return message


# def getCallCarMessage(data):
#     message = {
#       "type": "template",
#       "altText": "this is a template",
#       "template": {
#           "type": "buttons",
#           "text": f"請選擇至 {data['title']} 預約叫車時間",
#           "actions": [
#               {
#                "type": "datetimepicker",
#                "label": "預約",
#                "data": json.dumps(data),
#                "mode": "datetime"
#                }
#           ]
#       }
#     }
#     return message

#
#
# def getMRTVideoMessage():
#     message = dict()
#     message["type"] = "video"
#     message["originalContentUrl"] = F"{end_point}/static/taipei_101_video.mp4"
#     message["previewImageUrl"] = F"{end_point}/static/taipei_101.jpeg"
#     return message


# def getMRTSoundMessage():
#     message = dict()
#     message["type"] = "audio"
#     message["originalContentUrl"] = F"{end_point}/static/mrt_sound.m4a"
#     import audioread
#     with audioread.audio_open('static/mrt_sound.m4a') as f:
#         # totalsec contains the length in float
#         totalsec = f.duration
#     message["duration"] = totalsec * 1000
#     return message


#def getTaipei101ImageMessage(originalContentUrl=F"{end_point}/static/images.png"):
    #return getImageMessage(originalContentUrl)


#def getImageMessage(originalContentUrl):
    #message = dict()
    #message["type"] = "image"
    # message["originalContentUrl"] = originalContentUrl
    # message["previewImageUrl"] = originalContentUrl
    # return message


def replyMessage(payload):
    response = requests.post("https://api.line.me/v2/bot/message/reply",headers=HEADER,data=json.dumps(payload))
    return 'OK'


def pushMessage(payload):
    response = requests.post("https://api.line.me/v2/bot/message/push",headers=HEADER,data=json.dumps(payload))
    return 'OK'


# def getTotalSentMessageCount():
#     response = requests.get("https://api.line.me/v2/bot/message/quota/consumption",headers=HEADER)
#     return response.json()["totalUsage"]


# def getformMessage():
#     response = requests.get("https://covid-19.nchc.org.tw/api/covid19?CK=covid-19@nchc.org.tw&querydata=4001&limited=TWN")
#     date = response.json()[0]["a04"]
#     total_count = response.json()[0]["a05"]
#     count = response.json()[0]["a06"]
#     return F"日期：{date}, 人數：{count}, 確診總人數：{total_count}"


# def allowed_file(filename):
#     return '.' in filename and \
#            filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


# @app.route('/upload_file', methods=['POST'])
# def upload_file():
#     payload = dict()
#     if request.method == 'POST':
#         file = request.files['file']
#         print("json:", request.json)
#         form = request.form
#         age = form['age']
#         gender = ("男" if form['gender'] == "M" else "女") + "性"
#         if file:
#             filename = file.filename
#             img_path = os.path.join(UPLOAD_FOLDER, filename)
#             file.save(img_path)
#             print(img_path)
#             payload["to"] = my_line_id
#             payload["messages"] = [getImageMessage(F"{end_point}/{img_path}"),
#                 {
#                     "type": "text",
#                     "text": F"年紀：{age}\n性別：{gender}"
#                 }
#             ]
#             pushMessage(payload)
#     return 'OK'


# @app.route('/line_login', methods=['GET'])
# def line_login():
#     if request.method == 'GET':
#         code = request.args.get("code", None)
#         state = request.args.get("state", None)
#
#         if code and state:
#             HEADERS = {'Content-Type': 'application/x-www-form-urlencoded'}
#             url = "https://api.line.me/oauth2/v2.1/token"
#             FormData = {"grant_type": 'authorization_code', "code": code, "redirect_uri": F"{end_point}/line_login", "client_id": line_login_id, "client_secret":line_login_secret}
#             data = parse.urlencode(FormData)
#             content = requests.post(url=url, headers=HEADERS, data=data).text
#             content = json.loads(content)
#             url = "https://api.line.me/v2/profile"
#             HEADERS = {'Authorization': content["token_type"]+" "+content["access_token"]}
#             content = requests.get(url=url, headers=HEADERS).text
#             content = json.loads(content)
#             name = content["displayName"]
#             userID = content["userId"]
#             pictureURL = content["pictureUrl"]
#             statusMessage = content["statusMessage"]
#             print(content)
#             return render_template('profile.html', name=name, pictureURL=
#                                    pictureURL, userID=userID, statusMessage=
#                                    statusMessage)
#         else:
#             return render_template('login.html', client_id=line_login_id,
#                                    end_point=end_point)


if __name__ == "__main__":
    app.debug = True
    app.run()
