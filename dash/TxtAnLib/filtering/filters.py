import pandas as pd
from collections import Counter
import numpy as np
import matplotlib.pyplot as plt
from nltk.tokenize import TreebankWordTokenizer, ToktokTokenizer, TweetTokenizer
from tqdm.notebook import tqdm
from termcolor import colored
import datetime as dt
import seaborn as sns
from wordcloud import WordCloud
import json


def hash_retrieve(df: pd.DataFrame):
    '''
    Objective: The function takes as an object a df of tweets obtained via twarc and returns a generator object.
    Author: Luis Menéndez, Universitat Autonoma de Barcelona
    Date: Unknown
    '''
    for line, id in zip(df['entities.hashtags'], df['id']):
        if pd.isna(line):
            continue
        line = line.strip()
        data = json.loads(line)
        for hashtag in ensure_flattened(data):
            #print(hashtag['tag'],id)
            yield [hashtag['tag'], id]
            
            
def obtain_hashtags(df: pd.DataFrame):
    hashtags_df = pd.DataFrame(list(hash_retrieve(df)),
                 columns = ['tweet_hashtags', 'id'])
    
    hashtags_df = hashtags_df.groupby('id')['tweet_hashtags'].apply(lambda x: ','.join(x))
    
    df = df.merge(hashtags_df, how = 'left', left_on = 'id', right_on = 'id')
    df['tweet_hashtags'] = df['tweet_hashtags'].str.lower()
    

def f_authors(DF: pd.DataFrame, authors_list: list) -> pd.DataFrame:
    '''
    Objective: Recive as input a list of authors and returns a data frame with the tweets from these authors
    Author: Andrés Couble
    Date: June 3, 2022
    '''
    result = pd.DataFrame()
    for author in authors_list:
        df_1 = DF[DF['author.username'] == author]
        result = pd.concat([result,df_1])
        
    return result


def f_dates(DF: pd.DataFrame, start_time ="2020-10-31", end_time = "2022-04-12") -> pd.DataFrame:
    '''
    Objective: Recive an start time and end time and return the data frame only with the tweets in this period.
    Author: Andrés Couble
    Date: June 3, 2022
    '''
    df_1 = DF.copy()
    df_1['Date'] = df_1['created_at'].str[0:10]
    df_1['Date'] = pd.to_datetime(df_1['Date'])
    
    start = dt.datetime.strptime(start_time, '%Y-%m-%d')
    end = dt.datetime.strptime(end_time, '%Y-%m-%d')
    
    result = df_1[(df_1.Date>=start) & (df_1.Date<=end)]
    
    return result


def f_words(DF: pd.DataFrame, list_of_words: list) -> pd.DataFrame:
    '''
    Objective: Recive a list of words and return a data frame only with the tweets that contain one of these words.
    Author: Andrés Couble
    Date: June 3, 2022
    '''
    df_1 = DF.copy()
    df_1['total_count'] = 0
    for word in list_of_words:
        regex = '(?:^|\W)' + word + '(?:$|\W)'
        df_word = pd.DataFrame()
        df_word = df_1.dropna(subset = ['cleaned_text']).copy()
        df_word = df_word[df_word.cleaned_text.str.contains(regex)]
        df_word['count_' + str(word)] = 1
        df_1 = df_1.merge(df_word[['id','count_' + word]],how = "left",on = "id")
        df_1['count_' + word] = df_1['count_' + word].fillna(0)
        df_1['total_count'] += df_1['count_' + word]
        df_1 =  df_1.drop(['count_' + str(word)], axis = 1)
    
    result = df_1[df_1.total_count>0]
    result =  result.drop(['total_count'],axis = 1)
    
    return result


def f_hashtags(DF: pd.DataFrame, list_of_hashtags: list) -> pd.DataFrame:
    '''
    Objective: Recive a list of hashtags and return a data frame only with the tweets that contain one of these hashtags.
    Author: Andrés Couble
    Date: June 3, 2022
    '''
    df_1 = DF.copy()
    df_1['total_count'] = 0
    for hashtag in list_of_hashtags:
        df_hash = pd.DataFrame()
        df_hash = DF.dropna(subset = ['tweet_hashtags']).copy()
        df_hash = df_hash[df_hash.tweet_hashtags.str.contains(hashtag)]
        df_hash['count_' + str(hashtag)] = 1
        df_1 = df_1.merge(df_hash[['id','count_' + str(hashtag)]],how = "left",on = "id")
        df_1['count_' + str(hashtag)] = df_1['count_' + str(hashtag)].fillna(0)
        df_1['total_count'] += df_1['count_' + str(hashtag)]
        
        df_1 =  df_1.drop(['count_' + str(hashtag)], axis = 1)
    
    result = df_1[df_1.total_count>0]
    result =  result.drop(['total_count'],axis = 1)
    
    return result


def f_metrics(DF: pd.DataFrame, metric: str , treshold: float) -> pd.DataFrame:
    '''
    Objective: Filter tweets with certain number of RT, likes, quotes or respones metric: "Likes", "Retweets", "Quotes" or "Replies"
    Author: Andrés Couble
    Date: June 3, 2022
    '''
    if metric == "Likes":
        return DF[DF['public_metrics.like_count'] >= treshold].copy()
    
    if metric == "Retweets":
        return DF[DF['public_metrics.retweet_count'] >= treshold].copy()
    
    if metric == "Quotes":
        return DF[DF['public_metrics.quote_count'] >= treshold].copy()
    
    if metric == "Replies":
        return DF[DF['public_metrics.reply_count'] >= treshold].copy()
    

def f_location(DF: pd.DataFrame, list_of_locations: list) -> pd.DataFrame:
    '''
    Objective: Recive a list of words and return a data frame only with the tweets from authors that have one of these words in the location.
    Author: Andrés Couble
    Date: June 3, 2022
    '''
    df_1=DF.copy()
    df_1['total_count']=0
    df_1['author.location']=df_1['author.location'].str.lower()
    for location in list_of_locations:
        regex = '(?:^|\W)'+location+'(?:$|\W)'
        df_word=pd.DataFrame()
        df_word=df_1.dropna(subset=['author.location']).copy()
        df_word=df_word[df_word['author.location'].str.contains(regex)]
        df_word['count_'+str(location)]=1
        df_1=df_1.merge(df_word[['id','count_'+location]],how="left",on="id")
        df_1['count_'+location] = df_1['count_'+location].fillna(0)
        df_1['total_count']+=df_1['count_'+location]
        df_1= df_1.drop(['count_'+str(location)], axis=1)
    
    result=df_1[df_1.total_count>0]
    result= result.drop(['total_count'],axis=1)
    return result

def f_affiliation(DF,Affiliation="Unlabeled"):
    '''
    Objective: Recive a affiliation (Left, Right or Unlabeled) and return a DataFrame only with the tweets from authors of this affiliation.
    Author: Andrés Couble
    Date: June 10, 2022
    '''
    
    df_1=DF.copy()
    df_1['Label']=df_1['Label'].fillna("Unlabeled")
    return df_1[df_1['Label']==Affiliation]