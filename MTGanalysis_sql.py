import json as js
import sqlite3
import time

conn = sqlite3.connect('MTGanalysis_sql.sqlite')
cur = conn.cursor()

cur.executescript('''
DROP TABLE IF EXISTS Cards;
DROP TABLE IF EXISTS Artists;
DROP TABLE IF EXISTS Sets;
DROP TABLE IF EXISTS Rulings;

CREATE TABLE Artists (
id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
name TEXT UNIQUE
);

CREATE TABLE Cards (
id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
name TEXT NOT NULL,
artist_id INTEGER,
word_count INTEGER,
flavor_count INTEGER,
setname_id INTEGER,
date_released INTEGER,
reprint INTEGER,
oracle_id VARCHAR,
price INTEGER
);

CREATE TABLE Sets (
id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
set_type TEXT,
name TEXT NOT NULL UNIQUE
);

CREATE TABLE Rulings (
oracle_id VARCHAR,
Ruling_text TEXT
)

''')

fname = input('Filename for Cards file(include .json):')
fnamerulings = input('Filename for Rulings file(include .json):')
if len(fname) < 1:
    fname = 'scryfallcards_05_18_23.json'
    fnamerulings = 'scryfallrulings_05_19_23.json'

cards = js.loads(open(fname, encoding='utf8').read())
rulings = js.loads(open(fnamerulings, encoding = 'utf-8').read())

for card in cards:
    cardname = card['name']
    oracle_id = card.get('oracle_id')
    set_type = card.get('set_type')
    
    word_count = 0
    if card.get('card_faces'):
        words0 = len((card['card_faces'][0]['oracle_text']).split())
        words1 = len((card['card_faces'][1]['oracle_text']).split())
        word_count = words0 + words1
    elif card.get('oracle_text'): 
        word_count = len((card.get('oracle_text')).split())
    
    flavor_count = 0
    if card.get('card_faces'):
        try:
            flavorwords0 = len((card['card_faces'][0]['flavor_text']).split())
            flavorwords1 = len((card['card_faces'][1]['flavor_text']).split())
            flavor_count = flavorwords0 + flavorwords1
        except: flavor_count = 0
    elif card.get('flavor_text'): 
        flavor_count = len((card.get('flavor_text')).split())
    
    date = card['released_at']
    reprint = card['reprint']
    artist = card['artist']
    setname = card.get('set_name')
    if card.get('prices'):
        if card['prices']['usd'] is not None:
            price = card['prices']['usd'] 
        else: price = card['prices']['usd_foil']
    else: price = None
    
    cur.execute('''INSERT OR IGNORE INTO Artists (name) VALUES (?)''', (artist, ))
    cur.execute(''' SELECT id FROM Artists WHERE name = ?''', (artist, ))
    artist_id = cur.fetchone()[0]
   
    cur.execute('''INSERT OR IGNORE INTO Sets (name, set_type) VALUES (?,?)''', (setname, set_type))
    cur.execute('''SELECT id FROM Sets WHERE name = ?''', (setname, ))
    setname_id = cur.fetchone()[0]
    
    cur.execute('''INSERT INTO Cards (name, word_count, flavor_count, artist_id, date_released, reprint, setname_id, oracle_id, price) VALUES (?,?,?,?,?,?,?,?,?)''', (cardname, word_count, flavor_count, artist_id, date, reprint, setname_id, oracle_id, price))

print('cards done')
conn.commit()

for ruling in rulings:
    oracle_id = ruling['oracle_id']
    ruling_text = ruling['comment']
    
    cur.execute('''INSERT INTO Rulings (oracle_id, ruling_text) VALUES (?,?)''', (oracle_id, ruling_text))

print('rulings done')
conn.commit()

#FOR ANALYSIS
#count of cards each artist has done, used to be here: artist_count = dict() artist_count[artist] = artist_count.get(artist, 0)+1 cur.execute('''UPDATE Artists SET artist_count = (?) WHERE name = ?''', (artist_count[artist], artist))

#best way to ignore the 'duplicates' that are alt printings of the same card within a set might be the folloing sql query: 
#SELECT DISTINCT name, artist_id, setname_id
#FROM Cards
#WHERE name = 'Academy Loremaster'
