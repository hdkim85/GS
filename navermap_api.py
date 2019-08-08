# google map

import requests
import json
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd



#google map geocoding function

def geocoding(location):


    url="https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=AIzaSyApdxo0PerumoXiXKY1dQkjC_lavxSAID0" % (location)
    direction=requests.get(url)
    html=direction.text
    geo=json.loads(html)
    if geo['status']=='OK':
        lat=geo['results'][0]['geometry']['location']['lat']
        lng=geo['results'][0]['geometry']['location']['lng']
        lat=str(lat)
        lng=str(lng)
        location=lng+','+lat
        status=geo['status']
        return location, lat, lng, status
    else:
        lat=''
        lng=''
        location=''
        status=geo['status']
        return location, lat, lng, status


# duration function

def direction(start):
    ClientID = '348np9r8nu'
    ClientSecret= 'I5WvQIUd17MweksYkMzHMjUkI9SiXkKa2Gby2s7g'
    headers = {'X-NCP-APIGW-API-KEY-ID': ClientID, 'X-NCP-APIGW-API-KEY': ClientSecret}
    goal= '129.3694633, 35.495691' #gs엔텍
    params={'start':start, 'goal':goal}
    url='https://naveropenapi.apigw.ntruss.com/map-direction/v1/driving'
    direction=requests.get(url, headers=headers, params=params)
    html=direction.text
    direction_parse=json.loads(html)
    print('code:%s' % direction_parse['code'])
    if direction_parse['code'] == 0:
        duration=direction_parse['route']['traoptimal'][0]['summary']['duration']
        return duration
    else:
        duration=float('NaN')
        return duration


####################################################################################3




one=pd.read_csv('C:\\Users\\hdkim\\Anaconda3\\envs\\gsentech\\projectfile\\base1.csv', encoding='UTF-8')

location=one['주민등록주소(기본)']
id=one['직원id']



duration=[]
lat=[]
lng=[]
status=[]

for loca in location:
    start, lati, long, stat=geocoding(loca)
    lat.append(lati)
    lng.append(long)
    status.append(stat)
    time=direction(start)
    print(lati, long, time)
    duration.append(time)


id1=list(id)
path='./duration.csv'
table = pd.DataFrame({'id':id1, 'lat':lat, 'lng':lng, 'duration':duration})
table.to_csv(path, encoding="UTF-8", mode="w", index=False)

