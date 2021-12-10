import pandas as pd
import numpy as np
import tweepy
import requests
import base64
import json
import ast
import time
from ast import literal_eval


# https://iq.opengenus.org/geo-api-twitter/
def coordinates(val):
    # assign the values accordingly
    consumer_key = "sq8lFhE8jITyl7zIMirkgxHvZ"
    consumer_secret = "5fGBGoHltoEMi7O7xpl8rTStnGhDuOG74effc29DnCaWDx5ClG"
    access_token = "1263376219958992900-GeTK98sT3X2yERoow6wBMsevoegzsW"
    access_token_secret = "PQVADgfLShM1fEhP7r2WUFmKjQ1sk3WRcDG9qdB1rwzsJ"

    # authorization of consumer key and consumer secret
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

    # set access to user's access key and access secret
    auth.set_access_token(access_token, access_token_secret)

    # calling the api
    api = tweepy.API(auth)

    # Twitter ID of London
    id = val

    # fetching the location
    place = api.geo_id(id)

    return str(place.centroid)

lat = []
long = []

tweets_df = pd.read_csv("Data/Geo Tweets/shein_geo.csv", lineterminator='\n')

text = tweets_df['geo'].values
text

count = 0

for loc in text:
    if "coordinates" in loc:
        res = ast.literal_eval(loc)
        lat.append(res['coordinates']['coordinates'][1])
        long.append(res['coordinates']['coordinates'][0])
    elif "place_id" in loc:
        count = count + 1
        print(count)
        if count == 75:
            time.sleep(15 * 60)
            count = 0
        res = ast.literal_eval(loc)
        coors = coordinates(res['place_id'])
        coors_arr = literal_eval(coors)
        lat.append(coors_arr[1])
        long.append(coors_arr[0])


tweets_df['lat'] = lat
tweets_df['long'] = long

tweets_df.to_csv('shein_geo.csv', index=False) # change brand name