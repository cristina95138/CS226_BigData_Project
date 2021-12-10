import pandas as pd
import numpy as np
import tweepy
import requests
import base64
import json
import ast
import time


# https://iq.opengenus.org/geo-api-twitter/
def coordinates(val):
    # Define your keys from the developer portal
    consumer_key = 'sq8lFhE8jITyl7zIMirkgxHvZ'
    consumer_secret_key = '5fGBGoHltoEMi7O7xpl8rTStnGhDuOG74effc29DnCaWDx5ClG'

    # Reformat the keys and encode them
    key_secret = '{}:{}'.format(consumer_key, consumer_secret_key).encode('ascii')
    # Transform from bytes to bytes that can be printed
    b64_encoded_key = base64.b64encode(key_secret)
    # Transform from bytes back into Unicode
    b64_encoded_key = b64_encoded_key.decode('ascii')

    base_url = 'https://api.twitter.com/'
    auth_url = '{}oauth2/token'.format(base_url)
    auth_headers = {
        'Authorization': 'Basic {}'.format(b64_encoded_key),
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
    }
    auth_data = {
        'grant_type': 'client_credentials'
    }
    auth_resp = requests.post(auth_url, headers=auth_headers, data=auth_data)
    access_token = auth_resp.json()['access_token']

    geo_headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }

    geo_params = val

    geo_url = 'https://api.twitter.com/1.1/geo/id/' + geo_params + '.json'
    geo_resp = requests.get(geo_url, headers=geo_headers)

    geo_data = geo_resp.json()
    if geo_data['centroid']:
        geo_data = geo_data['centroid']
    else:
        geo_data = geo_data['coordinates']

    return geo_data

lat = []
long = []

tweets_df = pd.read_csv("Data/Geo Tweets/zara_geo.csv", lineterminator='\n')

text = tweets_df['geo'].values
text

count = 0

for loc in text:
    if "coordinates" in loc:
        res = ast.literal_eval(loc)
        lat.append(res['coordinates']['coordinates'][1])
        long.append(res['coordinates']['coordinates'][0])
    elif "place_id" in loc:
        ++count
        print(count)
        if count == 15:
            time.sleep(15 * 60)
            count = 0
        val = loc[14:30]
        coors = coordinates(val)
        lat.append(coors[1])
        long.append(coors[0])


tweets_df['lat'] = lat
tweets_df['long'] = long

tweets_df.to_csv('zara_geo.csv', index=False) # change brand name