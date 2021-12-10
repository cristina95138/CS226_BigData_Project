import tweepy
import time
import pandas as pd

bearer_token = ''

client = tweepy.Client(bearer_token, wait_on_rate_limit=True)

tweets = []

# (Shein OR SHEIN OR shein): 9,214
# (H&M OR HandM OR (H and M) OR h&m OR H&m OR h&M OR Handm OR handM): 11,366
# (Zara OR zara OR ZARA): 13,927
# (Boohoo OR boohoo OR BOOHOO): 4,562
# (Nike OR nike OR NIKE): 40,000
# (Adidas OR adidas OR ADIDAS): 24,422
# (Asos OR asos OR ASOS): 4,036
# (Chanel OR chanel OR CHANEL): 18,714
# (Victoria Secret OR Victorias Secret OR victoria secret OR Victoria secret OR Victorias secret OR victorias secret): 5,522
# (Gucci OR gucci OR GUCCI): 40,000

for response in tweepy.Paginator(client.search_recent_tweets,
                                 query = '(H&M OR HandM OR (H and M) OR h&m OR H&m OR h&M OR Handm OR handM) -is:retweet lang:en', # change brand name
                                 user_fields = ['username', 'public_metrics', 'description', 'location'],
                                 tweet_fields = ['created_at', 'geo', 'public_metrics', 'text'],
                                 expansions = 'author_id',
                                 start_time = '2021-12-02T11:00:00Z',
                                 end_time = '2021-12-08T12:00:00Z',
                                 max_results=100).flatten(limit=20000):
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

df.to_csv('h&m.csv', index=False) # change brand name

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