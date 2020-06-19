import tweepy
import pandas as pd
import json

consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)

def extractData(tweet,ent,text):
    s = ""
    for i in tweet.entities.get(ent,[{}]):
        s += (i[text]) +" "
    if s:
        s= s[:-1]
        print(s)
    return s

tweetData = {}
i =0
for tweets in tweepy.Cursor(api.search, q='#arsenal',include_entities=True, rpp=100,tweet_mode='extended').items(5000):
    sourceUrl = "https://twitter.com/"+tweets.user.screen_name+"/status/"+tweets.id_str
    singletweet = [tweets.full_text, tweets.user.screen_name, sourceUrl,"","","","",""]
    singletweet = {"text":tweets.full_text, "username": tweets.user.screen_name, "url":sourceUrl, "images":"","videos":"","embedded_URL": "","mentions":"","hashtags":""}
    i+=1
    ids = tweets.id
    try:
        if tweets.retweeted_status:
            sourceUrl = "https://twitter.com/"+tweets.retweeted_status.user.screen_name+"/status/"+tweets.retweeted_status.id_str
            tweet = api.get_status(tweets.retweeted_status.id_str,tweet_mode='extended')
            singletweet["text"] = tweet.full_text
            singletweet["username"] = tweet.user.screen_name
            singletweet["url"] = sourceUrl
            for ent in tweet.entities:
                if (ent == "hashtags"):
                    singletweet["hashtags"]= extractData(tweet,ent,'text')
                elif (ent == "user_mentions"):
                    singletweet["mentions"] = extractData(tweet,ent,'screen_name')
                elif (ent == "urls"):
                    singletweet["embedded_URL"] = extractData(tweet,ent,'expanded_url')
                elif (ent == "media"):
                    singletweet["images"] = extractData(tweet,ent,"media_url")
            try:
                for media in tweet.extended_entities["media"]:
                    singletweet["videos"] = media["video_info"]["variants"][1]["url"]
            except Exception as e:
                pass
    except AttributeError:
        for ent in tweets.entities:
            if (ent == "hashtags"):
                singletweet["hashtags"]= extractData(tweets,ent,'text')
            elif (ent == "user_mentions"):
                singletweet["mentions"] = extractData(tweets,ent,'screen_name')
            elif (ent == "urls"):
                singletweet["url"] = extractData(tweets,ent,'expanded_url')
            elif (ent == "media"):
                singletweet["images"] = extractData(tweets,ent,"media_url")
        try:
            for media in tweets.extended_entities["media"]:
                singletweet["videos"] = media["video_info"]["variants"][1]["url"]
        except:
            pass
    tweetData[i] = singletweet
    print(singletweet)

with open('./data/moddedData.json', 'w') as fp:
    json.dump(tweetData, fp)