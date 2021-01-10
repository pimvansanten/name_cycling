import re
import requests
from bs4 import BeautifulSoup
import pandas as pd

URL_PLAATSEN='https://nl.wikipedia.org/wiki/Lijst_van_Nederlandse_plaatsen'

def makesoup(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text,'html.parser')
    #empty text in superscripts to get rid of notes.
    sips = soup.find_all('sup')
    for sup in sips:
        sup.string = ''
    return soup

soup = makesoup(URL_PLAATSEN)

plaatsnamen=[]

content=soup.find(id='mw-content-text')
letter_heads=content.find_all('h2')
pars=letter_heads[0].find_all_next('p')
for par in pars:
    places = par.find_all('a')
    for place in places:
        plaatsnamen.append(place['title'])

