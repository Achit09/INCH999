import json
import requests

print ("請務必輸入完整OPN(EX:ICE2PCS01GXUMA1)")
res = input("輸入商品名稱：")

try:
    src = requests.get("https://www.infineon.com/products/opn/opnTranslator?term="+res+"&offset=0&max_results=2147483647&lang=en")
    data = json.loads(src.text)
    clist = data["opnJsonFragment_ps"]
    # print (clist)
    fullopn = clist[0]["opn"]
   

except json.decoder.JSONDecodeError:
    print(res,"查詢失敗，請輸入正確OPN")

    # ProductFamily = clist["ProductFamily"]
    # IspnName = clist["IspnName"]
    # for PB in clist["PriceBreaks"]:
    #     price = float((PB['Price'])*0.9)
    # price = round(price,2)
    # content = ( str(IspnName)+"\n"+str(CPN) +"  "+"$"+str(price))
    # return content