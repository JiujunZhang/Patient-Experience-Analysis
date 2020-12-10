#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  9 14:18:41 2020

@author: jiujunzhang
"""
import requests
import json
import pandas as pd
import time
import random
url_list = ['https://www.google.com/maps/preview/review/listentitiesreviews?authuser=0&hl=en&gl=us&pb=!1m2!1y9935909009206584397!2y1653338456928523551!2m2!1i8!2i10!3e1!4m5!3b1!4b1!5b1!6b1!7b1!5m2!1sWCXRX4e6JIXr5gKcnajABA!7e81']
for i in range(1,50):
    url_list.append('https://www.google.com/maps/preview/review/listentitiesreviews?authuser=0&hl=en&gl=us&pb=!1m2!1y9935909009206584397!2y1653338456928523551!2m2!1i'+str(i)+'8!2i10!3e1!4m5!3b1!4b1!5b1!6b1!7b1!5m2!1sWCXRX4e6JIXr5gKcnajABA!7e81')
###print(url_list)
c=[]
username = []
content = []
rating = []
for m in range(len(url_list)):
    text = requests.get(url_list[m]).text
    pretext = ')]}\''
    text = text.replace(pretext,'')
    soup = json.loads(text)
    conlist = soup[2]
    c.append(conlist)
    time.sleep(random.randint(1,3))
    for j in conlist:
        username. append(str(j[0][1]))
        content.append(str(j[3]))
        rating.append(str(j[4]))
        data = {'username': username, 'rating': rating, 'content': content}
        df= pd.DataFrame.from_dict(data)
df
df.to_csv('/Users/jiujunzhang/Desktop/HPE_dataset/Massachusetts_General_Hospital.csv',sep='\t', encoding='utf-8', header='true')

###for i in range(3):###set scroll down for 3 times (ASAP website design)
    ###browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
    ###time.sleep(4)
df.head()
# Calculate word count
df['word_count'] = df['content'].apply(lambda x: len(str(x).split(" ")))
# Calculate character count
df['char_count'] = df['content'].str.len()
def avg_word(content):
    words = content.split()
    return (sum(len(word) for word in words) / len(words))
# Calculate average words
df['avg_word'] = df['content'].apply(lambda x: avg_word(x))
# Import stopwords
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
stop_words = stopwords.words('english')
df['stopword_coun'] = df['content'].apply(lambda x: len([x for x in x.split() if x in stop_words]))
# Lower case all words
df['review_lower'] = df['content'].apply(lambda x: " ".join(x.lower() for x in x.split())) 
# Remove Punctuation
df['review_nopunc'] = df['review_lower'].str.replace('[^\w\s]', '')
# Remove Stopwords
df['review_nopunc_nostop'] = df['review_nopunc'].apply(lambda x: " ".join(x for x in x.split() if x not in stop_words))
# Return frequency of values
freq= pd.Series(" ".join(df['review_nopunc_nostop']).split()).value_counts()[:30]
other_stopwords = ['none','one','would' ]
df['review_nopunc_nostop_nocommon'] = df['review_nopunc_nostop'].apply(lambda x: "".join(" ".join(x for x in x.split() if x not in other_stopwords)))
!pip install textblob
# Import textblob
from textblob import Word
nltk.download('wordnet')

# Lemmatize final review format
df['cleaned_review'] = df['review_nopunc_nostop_nocommon']\
.apply(lambda x: " ".join([Word(word).lemmatize() for word in x.split()]))
print('Base review\n', df['content'][0])
print('\n------------------------------------\n')
print('Cleaned and lemmatized review\n', df['cleaned_review'][0])
# Calculate polarity
from textblob import TextBlob
df['polarity'] = df['cleaned_review'].apply(lambda x: TextBlob(x).sentiment[0])
# Calculate subjectivity
df['subjectivity'] = df['cleaned_review'].apply(lambda x: TextBlob(x).sentiment[1])
df[['cleaned_review', 'polarity', 'subjectivity']].head()
dta = df[['cleaned_review', 'polarity', 'subjectivity']]
dta.sort_values(by='polarity', ascending=True).head(30)
pip install wordcloud
# Python program to generate WordCloud 
  
# importing all necessery modules 
from wordcloud import WordCloud, STOPWORDS 
import matplotlib.pyplot as plt 
import pandas as pd 
  
# Reads 'Youtube04-Eminem.csv' file  
  
comment_words = '' 
stopwords = set(STOPWORDS) 
  
# iterate through the csv file 
for val in df.content: 
      
    # typecaste each val to string 
    val = str(val) 
  
    # split the value 
    tokens = val.split() 
      
    # Converts each token into lowercase 
    for i in range(len(tokens)): 
        tokens[i] = tokens[i].lower() 
      
    comment_words += " ".join(tokens)+" "
  
wordcloud = WordCloud(width = 800, height = 800, 
                background_color ='white', 
                stopwords = stopwords, 
                min_font_size = 10).generate(comment_words) 
  
# plot the WordCloud image                        
plt.figure(figsize = (8, 8), facecolor = None) 
plt.imshow(wordcloud) 
plt.axis("off") 
plt.tight_layout(pad = 0) 
  
plt.show() 


 