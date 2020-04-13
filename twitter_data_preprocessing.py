# -*- coding: utf-8 -*-
"""
Created on Fri Mar  6 08:45:35 2020

@author: Vedika Bansal
"""

import json
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import operator
import csv
import os
import matplotlib.pyplot as plt
from pathlib import Path

import re #regular expression
from textblob import TextBlob
import string
import preprocessor as p
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

emoticons_happy = set([
    ':-)', ':)', ';)', ':o)', ':]', ':3', ':c)', ':>', '=]', '8)', '=)', ':}',
    ':^)', ':-D', ':D', '8-D', '8D', 'x-D', 'xD', 'X-D', 'XD', '=-D', '=D',
    '=-3', '=3', ':-))', ":'-)", ":')", ':*', ':^*', '>:P', ':-P', ':P', 'X-P',
    'x-p', 'xp', 'XP', ':-p', ':p', '=p', ':-b', ':b', '>:)', '>;)', '>:-)',
    '<3'
    ])

# Sad Emoticons
emoticons_sad = set([
    ':L', ':-/', '>:/', ':S', '>:[', ':@', ':-(', ':[', ':-||', '=L', ':<',
    ':-[', ':-<', '=\\', '=/', '>:(', ':(', '>.<', ":'-(", ":'(", ':\\', ':-c',
    ':c', ':{', '>:\\', ';('
    ])

#Emoji patterns
emoji_pattern = re.compile("["
         u"\U0001F600-\U0001F64F"  # emoticons
         u"\U0001F300-\U0001F5FF"  # symbols & pictographs
         u"\U0001F680-\U0001F6FF"  # transport & map symbols
         u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
         u"\U00002702-\U000027B0"
         u"\U000024C2-\U0001F251"
         "]+", flags=re.UNICODE)

#combine sad and happy emoticons
emoticons = emoticons_happy.union(emoticons_sad)

#mrhod clean_tweets()
def clean_tweets(tweet):
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(tweet)

    #after tweepy preprocessing the colon left remain after removing mentions
    #or RT sign in the beginning of the tweet
    tweet = re.sub(r':', '', tweet)
    tweet = re.sub(r'‚Ä¶', '', tweet)
    #replace consecutive non-ASCII characters with a space
    tweet = re.sub(r'[^\x00-\x7F]+',' ', tweet)


    #remove emojis from tweet
    tweet = emoji_pattern.sub(r'', tweet)

    #filter using NLTK library append it to a string
    filtered_tweet = [w for w in word_tokens if not w in stop_words]
    filtered_tweet = []

    #looping through conditions
    for w in word_tokens:
        #check tokens against stop words , emoticons and punctuations
        if w not in stop_words and w not in emoticons and w not in string.punctuation:
            filtered_tweet.append(w)
    return ' '.join(filtered_tweet)

ifile = open('Depression-Cascading-Behaviour-Analysis-Twitter/Twitter_test_json.json', 'r')
tweet_list = []
all_data = []
i=0

for line in ifile:
    #print(line)
    i = i+1
    try:
        tweet = json.loads(line)
        tweet_list.append(tweet)

        
        t_id = tweet['id']
        t_hashtags = tweet['entities']['hashtags']      
        #t_user_mentions_id = tweet['entities']['user_mentions']['id']
        t_lang = tweet['lang']
        t_text = tweet['text']
        t_user_id = tweet['user']['id']
        t_user_description = tweet['user']['description']
        if tweet['place']!= None:
            t_country = tweet['place']['country']
        else:
            t_country = " "
        #clean_text = p.clean(tweet['text'])

        #call clean_tweet method for extra preprocessing
        filtered_tweet=clean_tweets(t_text)
        
        #pass textBlob method for sentiment calculations
        blob = TextBlob(filtered_tweet)
        sentiments = blob.sentiment

        #seperate polarity and subjectivity in to two variables
        polarity = sentiments.polarity
        subjectivity = sentiments.subjectivity
        mentions = ", ".join([mention['screen_name'] for mention in tweet['entities']['user_mentions']])      
        if(t_lang == 'en'):
            all_data.append([t_id, t_hashtags, t_lang, t_text, filtered_tweet, sentiments, polarity, subjectivity, t_user_id, t_user_description, t_country, tweet['favorite_count'], tweet['retweet_count'], mentions])
#            all_data.append([t_id, t_hashtags, t_lang, t_text, filtered_tweet, t_user_id, t_user_description, t_country])

    except:
        continue
    """
    if i>25:
        break
 
    """
df = pd.DataFrame(all_data, columns=['Id' ,'Hashtags','Language','Text', 'Filtered Text', 'Sentiment', 'Polarity', 'Subjectivity', 'User Id', 'User Description', 'Country', 'Favourite Count', 'Retweets Count', 'Mentions'])
#df = pd.DataFrame(all_data, columns=['Id' ,'Hashtags','Language','Text', 'Filtered Text', 'Sentiment', 'Polarity', 'Subjectivity', 'User Id', 'User Description', 'Country'])
#df = pd.DataFrame(all_data, columns=['Id' ,'Hashtags','Language','Text', 'Filtered Text', 'User Id', 'User Description', 'Country'])
df.to_csv('Twitter Data.csv')
print(df)
'''    
tweets = pd.DataFrame()
tweets['text'] = map(lambda tweet:tweet['text'],tweet_list)
tweets["lang"] = map(lambda tweet:tweet['lang'],tweet_list)
tweets["country"] = map(lambda tweet:tweet['place']['country'] if['place']!=None else None,tweet_list)

tweets_by_lang = tweets['lang'].value_counts()
'''

filename = 'Twitter Data.csv'

pathcsv = Path(filename).resolve()
pathcsv

data = pd.read_csv(str(pathcsv))
data.head()

df = data.iloc[:, 1:8]

user_ids = data['User Id']
list(user_ids)
tweets_by_users = user_ids.value_counts()

fig, ax = plt.subplots()
ax.tick_params(axis='x',labelsize=5)
ax.tick_params(axis='y',labelsize=5)
ax.set_xlabel("languages", fontsize=10)
ax.set_ylabel("number of tweets", fontsize=10)
ax.set_title("Top 5 users", fontsize=10, fontweight='bold')
tweets_by_users[:5].plot(ax=ax, kind='bar', color='blue')
