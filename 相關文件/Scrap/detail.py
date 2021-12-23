import googlemaps
from pprint import pprint
import time
API_KEY="AIzaSyAFThMqs2Spq3NKvAFRP-D0qZd6S4R3nWk"

gmaps=googlemaps.Client(API_KEY)
geocode_result=gmaps.geocode("台北市")
loc=geocode_result[0]['geometry']['location']
places=gmaps.places_nearby(keyword="火鍋",location=loc,radius=10000)
num=(len(places['results']))
j=1
while True :
    for n in range(0,num):
        ID=places['results'][n]['place_id']
        datalist = gmaps.place(place_id=ID)
        Data=datalist['result']
        phone=price_level=day=website='null'
        name=Data['name']
        address=Data['formatted_address']
        if 'formatted_phone_number' in Data:
            phone=Data['formatted_phone_number']
        num_comment=Data['user_ratings_total']
        if 'price_level' in Data:
            price_level=Data['price_level']
        avg_rating=Data['rating']
        if 'opening_hours' in Data:
            day=Data['opening_hours']['weekday_text']
        if 'website' in Data:
            website=Data['website']
        print('\n',j,": \n",name,":",address,phone,avg_rating,num_comment,price_level,'\n',day,'\n',website,'\n')
        if len(Data['reviews'])>=3:
            i=0
            while(i<3):
                reviews=Data['reviews'][i]['text']
                print(Data['reviews'][i]['rating'],":",reviews)
                i+=1
        else:
            i=0
            while i<len(Data['reviews']):
                reviews=Data['reviews'][i]['text']
                print(Data['reviews'][i]['rating'],":",reviews)
                i+=1
        j+=1
    time.sleep(10)
    if 'next_page_token' in places:
        places = gmaps.places_nearby(page_token=places['next_page_token'])
        num=(len(places['results']))
    else:
        break
