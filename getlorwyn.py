import urllib.request, urllib.error, urllib.parse
import json
import io
import time

urlroot = 'https://api.scryfall.com/cards/search?include_extras=true&include_variations=true&order=set&q=e%3A' 
set_data = []


setcodes = ['lrw', 'mor', 'shm', 'eve']

for code in setcodes:
    scryurl = urlroot + code + '&unique=prints'
    #print(scryurl)
    searchurl = urllib.parse.quote(scryurl, safe=':/=?+%&')
    #print(searchurl)
    link = urllib.request.urlopen(searchurl)
    jfile = link.read().decode()
    try:
        cards = json.loads(jfile)
    except:
        print('Error with json', cardurl)
        continue
    time.sleep(1.5)
    cards = cards['data']
    set_data.append(cards)
    time.sleep(1.5)
    print('got cards for ' + code)

    
