import urllib.request, urllib.error, urllib.parse
import json
import io
import time
import boto3
from datetime import datetime
import os

def lambda_handler(event, context):
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
        time.sleep(0.1)
        cards = cards['data']
        set_data.append(cards)
        time.sleep(0.1)
        print('got cards for ' + code)

    set_data = [set for sublist in set_data for set in sublist]   

    S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
    s3 = boto3.client("s3")

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_name = f"card_data_{timestamp}.json"
    s3.put_object(
        Bucket=S3_BUCKET_NAME,
        Key=file_name,
        Body=json.dumps(set_data),
        ContentType="application/json"
    )
    print(f"Uploaded {file_name} to {S3_BUCKET_NAME}")
