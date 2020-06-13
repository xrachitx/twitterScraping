import tweepy
import pandas as pd

consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)


df = pd.DataFrame(columns=['text', 'source', 'url'])
tweets = []
d = {}
singletweet=[]
i =0
for tweet in tweepy.Cursor(api.search, q='#covid19', rpp=100).items(5000):
    singletweet = [tweet.text, tweet.user.screen_name, tweet.source_url] 
    i+=1 
    d[i] = singletweet                
    tweets.append(singletweet)
    print(singletweet)
    print(i)

df = pd.DataFrame(d)
df.to_json("./data/moddedData.json")