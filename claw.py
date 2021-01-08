import json
import requests
from bs4 import BeautifulSoup
import pandas as pd


print ("請務必輸入完整OPN(EX:ICE2PCS01GXUMA1)")
res = input("輸入商品名稱：")


# 加入使用者資訊(如使用什麼瀏覽器、作業系統...等資訊)模擬真實瀏覽網頁的情況
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
                        (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'}

try:
    src = requests.get("https://so.szlcsc.com/global.html?k="+res, headers = headers)
    soup = BeautifulSoup(src.text,"lxml")

    # t1 = soup.find_all('table')
    names = soup.find_all(class_="two")
    price = soup.find_all(class_="price-warp")
    ProductName = list()
    Price = list()
    for name in names:
        ProductName.append(name.select_one("a").text.split())
    for prices in price:
        Price.append(prices.select_one("p").text.split() + prices.select_one("span").text.split())
        # Price.append(prices.select_one("span").text.split())
    # print(pd.DataFrame({
    #         '編號':ProductName,
    #         '價格':Price
    #         }))
    content = (ProductName, Price)
    print (content)
    

except json.decoder.JSONDecodeError:
    print(res,"查詢失敗，請輸入正確OPN")
