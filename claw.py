import json
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time


print ("請務必輸入完整OPN(EX:ICE2PCS01GXUMA1)")
res = input("輸入商品名稱：")

start_time = time.time() #開始時間
# 加入使用者資訊(如使用什麼瀏覽器、作業系統...等資訊)模擬真實瀏覽網頁的情況
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
                        (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'}

try:
    src = requests.get("https://so.szlcsc.com/global.html?k="+res)
    soup = BeautifulSoup(src.text,"lxml")
    names = soup.find_all(class_="two")
    price = soup.find_all(class_='ccd ccd-ppbbz',attrs={"data-startpurchasednumber":"1"})
    bands = soup.find_all(class_="brand-name")
    ProductNamelist = list()
    bandsNamelist = list()
    priceslist = list()
    content = list()
    # 取得搜尋數量 & 細節
    # print (price)

    for prices in price:
        priceslist.append(prices.text.split())
        
    for name in names:
        ProductNamelist.append(name.select_one("a").text.split())
   
    for band in soup.find_all(class_="brand-name"):
        bandsNamelist.append(band.text.split())

    dataframe = pd.DataFrame({
            'ProductName':ProductNamelist,
            'bandsName':bandsNamelist,
            'priceslist':priceslist,
            })

    content = str(dataframe.head(20))

    print(content)

    print("花費：" + str(time.time() - start_time) + "秒")
    
    

except json.decoder.JSONDecodeError:
    print(res,"查詢失敗，請輸入正確OPN")
