#This project uses databases downloaded from the Scryfall.com API 
#to conduct basic analysis of Magic: The Gathering cards and products 

import pandas as pd
import json as js

fname = input('Filename for Cards file(include .json):')
fnamerulings = input('Filename for Rulings file(include .json):')
if len(fname) < 1:
    fname = 'scryfall_cards_06_28_23.json'
if len(fnamerulings) < 1:
    fnamerulings = 'scryfall_rulings_06_28_23.json'

cardsdf = pd.DataFrame.from_dict(js.loads(open(fname, encoding='utf8').read()))
rulingsdf = pd.DataFrame.from_dict(js.loads(open(fnamerulings, encoding = 'utf-8').read()))

def set_columns(x):
    dictkeep = {
        'comment': 'Number of Rulings',
        'name': 'Card Name',
        'oracle_id': 'Oracle_ID',
        'set_type': 'Set Type',
        'oracle_text': 'Card Text',
        'Price': 'Price',
        'released_at': 'Release Date',
        'reprint': 'Reprint',
        'artist': 'Artist',
        'set_name': 'Set Name',
        'flavor_text': 'Flavor Text',
        'Word Count': 'Word Count',
        'Flavor Word Count': 'Flavor Word Count'
    }
    df = x.rename(columns=dictkeep).drop(labels = [name for name in x.columns if name not in dictkeep], axis=1)
    return df
    
def wordcount(x):
    text = x.split()
    return len(text)

def dfcwordcount(x):
    text1 = x[0]['oracle_text']
    text2 = x[1]['oracle_text']
    return  len((text1 + text2).split())

def dfcflavorcount(x):
    try:
        text1 = x[0]['flavor_text']
        text2 = x[1]['flavor_text']
        return len((text1 + text2).split())
    except:
        return 0

def priceget(x):
    nprice = x['usd']
    if nprice is None:
        nprice = x['usd_foil']
    return nprice

#create and fix columns using the above functions - needed because of the nested/listed dictionaries in the json
cardsdf['Word Count'] = (cardsdf['oracle_text'].map(wordcount, na_action='ignore')).add(cardsdf['card_faces'].map(dfcwordcount, na_action='ignore'), fill_value=0)
cardsdf['Flavor Word Count'] = (cardsdf['flavor_text'].map(wordcount, na_action='ignore')).add(cardsdf['card_faces'].map(dfcflavorcount, na_action='ignore'), fill_value=0)
cardsdf['Price'] = cardsdf['prices'].map(priceget, na_action='ignore')
cardsdf['Price'] = pd.to_numeric(cardsdf['Price'], errors = 'coerce')

#merge in the 'Rulings' data, then use my set_columns function to create the final dataframe
rcountdf = pd.DataFrame(rulingsdf['comment'].groupby(rulingsdf['oracle_id']).count())
newdf = rcountdf.merge(cardsdf, how='outer', on='oracle_id')

cardsdf = set_columns(newdf)

#make a new dataframe for an analysis of word counts, grouped by set, over time (threw in number of artists per set too for fun)
cardsdf = cardsdf.drop_duplicates(subset=['Oracle_ID', 'Set Name'])
settest = cardsdf['Set Name'][(cardsdf['Set Type']=='expansion') | (cardsdf['Set Type']=='core')].dropna()
wordsinset = cardsdf['Word Count'].groupby(settest, sort='ascending').sum()
dateofset = cardsdf['Release Date'].groupby(settest).min()
cardsinset = cardsdf['Card Name'].groupby(settest).count()
artistsinset = cardsdf['Artist'].groupby(settest).nunique()
#leaving artists out for now, its complicated because of the drop-duplicates above (multiple artists on same card in some sets, showcase versions etc)
rulingsinset = cardsdf['Number of Rulings'].groupby(settest).sum()

analysisdf = pd.DataFrame({'Release Date': dateofset,
                           'Cards in Set': cardsinset,
                            'Word Count': wordsinset,
                            'Total Rulings in Set': rulingsinset}, index=wordsinset.index)

analysisdf['Words per Card'] = analysisdf['Word Count']/analysisdf['Cards in Set']
analysisdf['Rulings per Card'] = (analysisdf['Total Rulings in Set'])/(analysisdf['Cards in Set'])

print(analysisdf.head())

analysisdf.to_excel('mtgdataanalysis_pandas.xlsx')
print('Excel File Written into working directory')

