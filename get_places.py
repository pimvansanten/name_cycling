import re
import requests
from bs4 import BeautifulSoup
import pandas as pd
import json

BASE_URL='https://nl.wikipedia.org'
URL_NEDERLAND='/wiki/Lijst_van_Nederlandse_plaatsen'
URL_LIMBURG="/wiki/Lijst_van_steden_en_dorpen_in_Limburg_(Nederland)"

def makesoup(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text,'html.parser')
    #empty text in superscripts to get rid of notes.
    sips = soup.find_all('sup')
    for sup in sips:
        sup.string = ''
    return soup

def get_place_details(url):
    s2=makesoup(BASE_URL+url)
    tabel = s2.find(class_="infobox")
    if tabel:
        df=pd.read_html(str(tabel))[0]
        try:
            if df.loc[0,0].split()[0].lower() in ['dorp','plaats','gemeente','stad','gehucht']:
                naam=tabel.find('caption').find('b').string
                coord_link=tabel.find(id='text_coordinates').find('a')['href']
                coord_string=re.match(r".+params=([\w\.]+)_type.+",coord_link).group(1)
                coor_nums=[float(d) for d in coord_string.split('_') if not d.isalpha()]
                lat=coor_nums[0]+coor_nums[1]/60
                mid=int(len(coor_nums)/2)
                lon=coor_nums[mid]+coor_nums[mid+1]/60
                if mid==3:
                    lat=lat+coor_nums[mid-1]/3600
                    lon=lon+coor_nums[mid+2]/3600
            else:
                naam = None
                lat=None
                lon=None
        except:
            naam = None
            lat=None
            lon=None
    else:
        naam = None
        lat=None
        lon=None
    return naam, (lat,lon)

def get_plaatsen_nederland():
    #div with the 
    plaatsen={}
    soup = makesoup(BASE_URL+URL_NEDERLAND)
    content=soup.find(id='mw-content-text')
    letter_heads=content.find_all('h2')
    pars=letter_heads[0].find_all_next('p')
    for par in pars:
        places = par.find_all('a')
        for place in places:
            url=place['href']
            naam, coords=get_place_details(place['href'])
            if naam:
                plaatsen[naam]=coords
    return plaatsen

def get_plaatsen_limburg():
    plaatsen={}
    soup = makesoup(BASE_URL+URL_LIMBURG)
    letter_heads=soup.find_all('h2')
    for lh in letter_heads:
        table=lh.find_next('table')
        if table:
            for li in table.find_all('li'):
                place=li.find('a')
                naam, coords=get_place_details(place['href'])
                if naam:
                    plaatsen[naam]=coords
    return plaatsen

plaatsen=get_plaatsen_limburg()

with open(f'plaatsen_limburg.json', 'w') as f:
    json.dump(plaatsen, f)