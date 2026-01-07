def getcards(deckfile):
    '''
    Description// Takes a decklist and outputs a list of Python objects derived from JSON from the Scryfall API, where each object represents a card in the input decklist
    
    Params// decklist: csv file of cards formatted as "1 <cardname>"
    '''
    import urllib.request, urllib.error, urllib.parse
    import json
    import io
    scryurl = 'https://api.scryfall.com/cards/'
    decklist = io.open(deckfile,'r',encoding='utf8')
    card_data = []
    for card in decklist:
        if card[0].isdigit(): 
            quantity = card[0]
            pass
        else: continue
        cardurl = '+'.join(card.split()[1:]).split('//')[0]
        #print(cardurl)
        searchurl = 'https://api.scryfall.com/cards/named?exact=' + cardurl
        #print(searchurl)
        searchurl = urllib.parse.quote(searchurl, safe=':/=?+')
        #print(searchurl)
        #print(type(searchurl))
        link = urllib.request.urlopen(searchurl)
        jfile = link.read().decode()
        try:
            card = json.loads(jfile)
        except:
            print('Error with json', cardurl)
            continue
        time.sleep(0.1)

        rulings_link = urllib.request.urlopen(card['rulings_uri'])
        rjfile = rulings_link.read().decode()
        try:
            rulings = json.loads(rjfile)
        except:
            print('Error with json', cardurl)
            continue

        card['Rulings'] = len(rulings['data'])
        card['Quantity'] = quantity
        print(quantity)
        card_data.append(card)
        time.sleep(0.1)
    print('Returned Data From ', len(card_data), ' Cards')
    return card_data