import tweepy
import time
import pandas as pd

bearer_token = 'AAAAAAAAAAAAAAAAAAAAAM%2FzUwEAAAAAK1aKH7L%2BIXluoV0Sxj96sonqgUM%3DjfbNB0zXvz5dxUxCMDQi5F9bFGZR6BJjkyPDhig3vS7NG4kKDk'

client = tweepy.Client(bearer_token, wait_on_rate_limit=True)

tweets = []

for response in tweepy.Paginator(client.search_recent_tweets,
                                 query = 'Shein lang:en', # change brand name
                                 user_fields = ['username', 'public_metrics', 'description', 'location'],
                                 tweet_fields = ['created_at', 'geo', 'public_metrics', 'text'],
                                 expansions = 'author_id',
                                 start_time = '2021-12-02T00:00:00Z',
                                 end_time = '2021-12-05T00:00:00Z',
                                 max_results=100).flatten(limit=1200):
    time.sleep(1)
    tweets.append(response)

results = []
user_dict = {}

# Loop through each response object
for response in tweets:
    # Take all of the users, and put them into a dictionary of dictionaries with the info we want to keep
    for user in response.includes['users']:
        user_dict[user.id] = {'username': user.username,
                              'followers': user.public_metrics['followers_count'],
                              'tweets': user.public_metrics['tweet_count'],
                              'description': user.description,
                              'location': user.location
                             }
    for tweet in response.data:
        # For each tweet, find the author's information
        author_info = user_dict[tweet.author_id]
        # Put all of the information we want to keep in a single dictionary for each tweet
        results.append({'author_id': tweet.author_id,
                       'username': author_info['username'],
                       'author_followers': author_info['followers'],
                       'author_tweets': author_info['tweets'],
                       'author_description': author_info['description'],
                       'author_location': author_info['location'],
                       'text': tweet.text,
                       'created_at': tweet.created_at,
                       'retweets': tweet.public_metrics['retweet_count'],
                       'replies': tweet.public_metrics['reply_count'],
                       'likes': tweet.public_metrics['like_count'],
                       'quote_count': tweet.public_metrics['quote_count']
                      })

# Change this list of dictionaries into a dataframe
df = pd.DataFrame(results)

df.to_csv('shein.csv', index=False) # change brand name

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