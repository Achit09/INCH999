
import os
import requests
import json

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    LineBotApiError, InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
SECRET = os.environ.get('SECRET')

line_bot_api = LineBotApi(ACCESS_TOKEN)
handler = WebhookHandler(SECRET)


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    
    except LineBotApiError as e:
        print("Catch exception from LINE Messaging API: %s\n" % e.message)
        for m in e.error.details:
            print("ERROR is %s: %s" % (m.property, m.message))
        print("\n")

    except InvalidSignatureError:
        abort(400)

    return 'OK'

#MCHP查價格
def MCHP(result):
    src = requests.get("https://www.microchipdirect.com/api/Product/ProductInfo?CPN="+result)
    data = json.loads(src.text)
    clist = data["products"]
    content = ""
    for CPN in clist:
        repons = (CPN["CPN"])
        repons2 = CPN["BusinessPricingInfo"]
        for Value in repons2:
            Price = Value["Value"]
        content += str(repons)+("  ")+str(Price)+("\n")
    return content

#IFX查價格
def Infineon(result):
    src = requests.get("https://www.infineon.com/shop/products/pricing-availability/"+result)
    data = json.loads(src.text)
    clist = data["ProductInfo"]
    CPN = clist["ManufacturerPartNumber"]
    # ProductFamily = clist["ProductFamily"]
    IspnName = clist["IspnName"]
    for PB in clist["PriceBreaks"]:
        price = float((PB['Price'])*0.9)
    price = round(price,2)
    content = ( str(IspnName)+"\n"+str(CPN) +"  "+"$"+str(price))
    return content


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # line_bot_api.reply_message(event.reply_token,TextSendMessage(text= "稍等，搜尋中"))
    result = event.message.text
    content = MCHP(result)
    line_bot_api.reply_message(event.reply_token,TextSendMessage(text= content))


if __name__ == "__main__":
    app.run()