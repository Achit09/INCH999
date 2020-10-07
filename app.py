from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    LineBotApiError, InvalidSignatureError
)

from linebot.models import (
    SourceUser,SourceGroup,SourceRoom,LeaveEvent,JoinEvent,
    TemplateSendMessage,PostbackEvent,AudioMessage,
    ButtonsTemplate,ButtonsTemplate,
    ImageMessage,URITemplateAction,MessageTemplateAction,ConfirmTemplate,
    PostbackTemplateAction,ImageSendMessage,MessageEvent, TextMessage, 
    TextSendMessage,StickerMessage, StickerSendMessage,
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
# album_id = os.getenv('album_id',None)
# access_token = os.getenv('access_token',None)
# refresh_token = os.getenv('refresh_token',None)
client = ImgurClient(client_id, client_secret)
# url = os.getenv('firebase_bot',None)

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
    # profile = line_bot_api.get_profile(event.source.user_id)
    # tem_name = str(profile.display_name)
    # img_id = 1
    return 0
    

@handler.add(MessageEvent, message=TextMessage)
def handle_msg_text(event):
    content = event.message.text  
    if event.message.text == 'ts':
        buttonsTemplate = TemplateSendMessage(
                alt_text='The template',
                template=ButtonsTemplate(
                    title='目前主題為',
                    text= content,
    #                thumbnail_image_url= imgur_ran(),
                    actions=[
                        MessageTemplateAction(
                            label='修改主題',
                            text='修改主題'
                        ),
                    MessageTemplateAction(
                            label='imgur scrap',
                            text='imgur scrap'
                        )
                    ]
                )
            )
            # message = TextSendMessage(text=content)
        line_bot_api.reply_message(event.reply_token,buttonsTemplate)

if __name__ == "__main__":
    app.run()