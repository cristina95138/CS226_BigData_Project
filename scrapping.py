import tweepy
import time
import pandas as pd



client = tweepy.Client(bearer_token, wait_on_rate_limit=True)

tweets = []

# (Shein OR SHEIN OR shein)
# (H&M OR HandM OR (H and M) OR h&m OR H&m OR h&M OR Handm OR handM)
# (UNIQLO OR Uniqlo OR uniqlo)
# (Zara OR zara OR ZARA)
# (Forever 21 OR forever 21 OR FOREVER 21)
# (Fashion Nova OR fashion nova OR Fashion nova OR fashion Nova OR FASHION NOVA)
# (Boohoo OR boohoo OR BOOHOO)
# (Missguided OR missguided OR MISSGUIDED)


for response in tweepy.Paginator(client.search_recent_tweets,
                                 query = '(Missguided OR missguided OR MISSGUIDED) -is:retweet lang:en', # change brand name
                                 user_fields = ['username', 'public_metrics', 'description', 'location'],
                                 tweet_fields = ['created_at', 'geo', 'public_metrics', 'text'],
                                 expansions = 'author_id',
                                 start_time = '2021-12-02T00:00:00Z',
                                 end_time = '2021-12-07T12:00:00Z',
                                 max_results=100).flatten(limit=15000):
    #time.sleep(1)
    tweets.append(response)

results = []
user_dict = {}

# Loop through each response object
for response in tweets:
    # Put all of the information we want to keep in a single dictionary for each tweet
    results.append({'author_id': response.author_id,
                    'text': response.text,
                    'geo': response.geo,
                    'created_at': response.created_at,
                    'retweets': response.public_metrics['retweet_count'],
                    'replies': response.public_metrics['reply_count'],
                    'likes': response.public_metrics['like_count'],
                    'quote_count': response.public_metrics['quote_count']
                    })

# Change this list of dictionaries into a dataframe
df = pd.DataFrame(results)

df.to_csv('missguided.csv', index=False) # change brand name

'''
client = tweepy.Client(bearer_token='the token')

# Replace with your own search query
query = 'shein -is:retweet'

tweets = client.search_recent_tweets(query=query, tweet_fields=['context_annotations', 'created_at'], max_results=100)

for tweet in tweets.data:
    print(tweet.text)

auth = tweepy.OAuthHandler("key", "secret")
##auth.set_access_token("bearer_token", access_token_secret)

api = tweepy.API(auth)

public_tweets = api.home_timeline()
for tweet in public_tweets:
    print(tweet.text)
'''