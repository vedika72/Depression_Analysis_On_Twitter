# -*- coding: utf-8 -*-
"""
Created on Fri Mar  6 08:45:35 2020

@author: HP
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

"""
df = pd.DataFrame(all_data, columns=['ID' ,'text','country'])
print(df)
ifile.close()    
"""

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
        
        if(t_lang == 'en'):
            all_data.append([t_id, t_hashtags, t_lang, t_text, t_user_id, t_user_description, t_country])

    except:
        continue
    #if i>25:
        #break
df = pd.DataFrame(all_data, columns=['Id' ,'Hashtags','Language','Text', 'User Id', 'User Description', 'Country'])
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
