import requests
import googlemaps
from pprint import pprint
import time
API_KEY=" " #api key
gmaps=googlemaps.Client(API_KEY)
geocode_result=gmaps.geocode("北投區") #解析地址資訊
loc=geocode_result[0]['geometry']['location']
places=gmaps.places_nearby(keyword="北投區小火鍋",location=loc,radius=4000,type="restaurant")
num=(len(places['results']))
i=0
print('[')
while True :
    for n in range(0,num):
        ID=places['results'][n]['place_id']#取得店家ID
        url = "https://maps.googleapis.com/maps/api/place/details/json?place_id="
        payload={}
        headers = {}
        response = requests.request("GET", url+ID+"&key=??????????", headers=headers, data=payload)
        print(response.text,',')
        i+=1
            
    if 'next_page_token' in places:
        time.sleep(2+i)
        places = gmaps.places_nearby(page_token=places['next_page_token'])#下一頁最多只能爬三頁,60筆
        num=(len(places['results']))
    else:
        print(']')
        print('i : ',i)
        break
