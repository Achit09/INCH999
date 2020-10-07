from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    LineBotApiError, InvalidSignatureError
)
from firebase import firebase
from linebot.models import (
    SourceUser,SourceGroup,SourceRoom,LeaveEvent,JoinEvent,
    TemplateSendMessage,PostbackEvent,AudioMessage,LocationMessage,
    ButtonsTemplate,LocationSendMessage,AudioSendMessage,ButtonsTemplate,
    ImageMessage,URITemplateAction,MessageTemplateAction,ConfirmTemplate,
    PostbackTemplateAction,ImageSendMessage,MessageEvent, TextMessage, 
    TextSendMessage,StickerMessage, StickerSendMessage,DatetimePickerTemplateAction,
    CarouselColumn,CarouselTemplate
)
from imgurpython import ImgurClient
import re
import requests
import random
import os,tempfile
import json


app = Flask(__name__)

client_id = os.getenv('client_id',None)
client_secret = os.getenv('client_secret',None)
album_id = os.getenv('album_id',None)
access_token = os.getenv('access_token',None)
refresh_token = os.getenv('refresh_token',None)
client = ImgurClient(client_id, client_secret, access_token, refresh_token)
url = os.getenv('firebase_bot',None)
fb = firebase.FirebaseApplication(url,None)
line_bot_api = LineBotApi(os.getenv('LINE_CHANNEL_ACCESS_TOKEN',None))
handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET', None))



@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body,signature)
    except LineBotApiError as e:
        print("Catch exception from LINE Messaging API: %s\n" % e.message)
        for m in e.error.details:
            print("ERROR is %s: %s" % (m.property, m.message))
        print("\n")
    except InvalidSignatureError:
        abort(400)
    return 'OK'


def img_describe(text,img_id):#紀錄describe 把firebase裡面describe修改
    t = fb.get('/pic',None)
    tex = text[1:]
    patterns = str(img_id)+'.*'
    if re.search(patterns,text.lower()):
        count = 1
        for key,value in t.items():
            if count == len(t):#取得最後一個dict項目
                data2 = {'describe': str(tex), 'id': value['id'], 'user': value['user']}
                fb.put(url+'/pic/',data=data2,name=key)
            count+=1
        return 'Image紀錄程功'

def get_image(text):
    if len(text) <4:
        return None
    else:
        tex = text[3:]
        t = fb.get('/pic',None)
        for value in t.items():
            if value['describe'] == tex:
                
                client = ImgurClient(client_id, client_secret)
                images = client.get_album_images(album_id)
                img_id = int(value['id'])-1  #從firebase取出來是字串
                url = images[img_id].link
                image_message = ImageSendMessage(
                        original_content_url=url,
                        preview_image_url=url
                )
                return image_message

def check_pic(img_id):
    Confirm_template = TemplateSendMessage(
    alt_text='要給你照片標籤描述嗎?',
    template=ConfirmTemplate(
    title='注意',
    text= '要給你照片標籤描述嗎?\n要就選Yes,並且回覆\n-->id+描述訊息(這張照片id是'+ str(img_id) +')',
    actions=[                              
            PostbackTemplateAction(
                label='Yes',
                text='I choose YES',
                data='action=buy&itemid=1'
            ),
            MessageTemplateAction(
                label='No',
                text='I choose NO'
            )
        ]
    )
    )
    return Confirm_template



@handler.add(JoinEvent)
def handle_join(event):
    newcoming_text = "我會當做個位小幫手～"
#    謝謝邀請我這個ccu linebot來至此群組！！我會當做個位小幫手～<class 'linebot.models.events.JoinEvent'>
    line_bot_api.reply_message(
            event.reply_token,
            TextMessage(text=newcoming_text + str(JoinEvent))
        )

@handler.add(MessageEvent,message=ImageMessage)
def handle_msg_img(event):
    profile = line_bot_api.get_profile(event.source.user_id)
    tem_name = str(profile.display_name)
    img_id = 1
    t = fb.get('/pic',None)
    if t!=None:
        count = 1
        for value in t.items():
            if count == len(t):#取得最後一個dict項目
                img_id = int(value['id'])+1
            count+=1
    try:
        message_content = line_bot_api.get_message_content(event.message.id)
        with tempfile.NamedTemporaryFile(prefix='jpg-', delete=False) as tf:
            for chunk in message_content.iter_content():
                tf.write(chunk)
            fb.post('/pic',{'id':str(img_id),'user':tem_name,'describe':''})
            tempfile_path = tf.name
        path = tempfile_path
        client = ImgurClient(client_id, client_secret, access_token, refresh_token)
        config = {
            'album': album_id,
            'name' : img_id,
            'title': img_id,
            'description': 'Cute kitten being cute on'
        }
        client.upload_from_path(path, config=config, anon=False)
        os.remove(path)
        image_reply = check_pic(img_id)
        line_bot_api.reply_message(event.reply_token,[TextSendMessage(text='上傳成功'),image_reply])
    except  Exception as e:
        t = '上傳失敗'+str(e.args)
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=t))

@handler.add(MessageEvent, message=TextMessage)
def handle_msg_text(event):
    content = event.message.text  
    # profile = line_bot_api.get_profile(event.source.user_id)
    # user_name = profile.display_name
    # picture_url = profile.picture_url

    message = TextSendMessage(text=content)
    line_bot_api.reply_message(event.reply_token,message)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)