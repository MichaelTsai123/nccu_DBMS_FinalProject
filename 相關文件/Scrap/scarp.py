import googlemaps
from pprint import pprint
import time 

API_KEY="" #api key

gmaps=googlemaps.Client(API_KEY)
geocode_result=gmaps.geocode("北投區") #解析地址資訊
loc=geocode_result[0]['geometry']['location']
places=gmaps.places_nearby(keyword="北投區小火鍋",location=loc,radius=5000)#搜尋北投區附近5公里“北投區小火鍋”

num=(len(places['results']))
i=0
while True :
    for n in range(0,num):
        i+=1
        ID=places['results'][n]['place_id']#取得店家ID
        datalist = gmaps.place(place_id=ID)#利用ID獲得更詳細店家資訊
        Data=datalist['result']
        pprint(Data)
    print('i : ',i)
    if 'next_page_token' in places:
        time.sleep(2+i)
        places = gmaps.places_nearby(page_token=places['next_page_token'])#下一頁最多只能爬三頁,60筆
        num=(len(places['results']))
    else:
        break
