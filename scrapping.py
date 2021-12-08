import tweepy
from twitter_authentication import bearer_token
import time
import pandas as pd

'''
client = tweepy.Client(bearer_token, wait_on_rate_limit=True)

print("things worked till here")

shein_tweets = []
for response in tweepy.Paginator(client.search_all_tweets, 
                                 query = 'SHEIN -is:retweet lang:en',
                                 start_time = '2021-12-05T00:00:00Z',
                                 end_time = '2021-12-01T00:00:00Z',
                              max_results=500):
    time.sleep(1)
    shein_tweets.append(response)
print("getting tweets done")
print(shein_tweets[0].data[0])
print(shein_tweets[0].includes['users'][2])
'''

client = tweepy.Client(bearer_token='the token')

# Replace with your own search query
query = 'shein -is:retweet'

tweets = client.search_recent_tweets(query=query, tweet_fields=['context_annotations', 'created_at'], max_results=100)

for tweet in tweets.data:
    print(tweet.text)

'''auth = tweepy.OAuthHandler("key", "secret")
##auth.set_access_token("bearer_token", access_token_secret)

api = tweepy.API(auth)

public_tweets = api.home_timeline()
for tweet in public_tweets:
    print(tweet.text)
'''