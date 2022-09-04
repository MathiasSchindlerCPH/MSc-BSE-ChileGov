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


def word_cloud(DF: pd.DataFrame, number_of_words = 100):
    '''
    Objective: Plot a word cloud of the data set
    Author: Andrés Couble
    Date: June 3, 2022
    '''
    DF['cleaned_text']=DF['cleaned_text'].fillna(str(""))
    string = " ".join(list(DF['cleaned_text']))
    wordcloud = WordCloud(max_font_size = 100, max_words = number_of_words, background_color = "white",min_font_size = 10,width = 1600,height = 800).generate(string)
    plt.figure(figsize = (20, 10))
    plt.imshow(wordcloud, interpolation = "bilinear")
    plt.axis("off")
    plt.show()
    

def top_words(DF: pd.DataFrame, number_of_words = 100) -> list:
    '''
    Objective: Print the most common words in the data frame.
    Author: Andrés Couble
    Date: June 3, 2022
    '''
    string = " ".join(list(DF['cleaned_text']))
    split_it = string.split()
    counter = Counter(split_it)
    most_occur = counter.most_common(number_of_words)
    print(most_occur)
    
    
def top_authors(DF: pd.DataFrame, number_of_authors = 100) -> list:
    '''
    Objective: Print the most occuring authors
    Author: Andrés Couble
    Date: June 3, 2022
    '''
    count = Counter(list(DF['author.username']))
    most_occur = count.most_common(number_of_authors)
    print(most_occur)


def top_hashtags(DF: pd.DataFrame, number_print = 100, number_plot = 20) -> list:
    '''
    Objective: Print the common hashtags and plot how often are used each one.
    Author: Andrés Couble
    Date: June 3, 2022
    '''
    hasht = []
    for i in DF.index:
        try:
            hasht.append(DF['tweet_hashtags'][i].split(","))
        except:
            hasht.append([])

    DF['list_hashtags'] = hasht
    hashtags = []
    for ix in DF.index:
        hashtags+=DF['list_hashtags'][ix]
    print("There are {} different hashtags.".format(len(list(set(hashtags)))))
    print('\n')
    count = Counter(hashtags)
    most_occur = count.most_common(number_print)
    print(most_occur)
    
    data = most_occur[0:number_plot]

    n_groups = len(data)

    vals = [x[1] for x in data]
    legends = [x[0] for x in data]
    legends = ['#' + hashtag for hashtag in legends]

    #fig, ax = plt.subplots()

    index = np.arange(n_groups)
    bar_width = 0.25
    plt.figure(figsize = (20, 10))
    rects1 = plt.bar(index, vals, bar_width,
                     color = 'b',
                     label = 'Ocurrences')

    plt.xlabel('Hashtags', fontsize=18)
    plt.ylabel('Hashtags Count', fontsize=18)
    plt.title('Top Hashtags', fontsize=18)
    plt.xticks(index + bar_width, legends, fontsize = 18)
    plt.xticks(rotation = 90)
    plt.yticks(fontsize = 18)
    #plt.legend(fontsize = 18)
    #plt.tight_layout()
    #plt.show()


def pday_tweets(DF: pd.DataFrame):
    '''
    Objective: Plot the number of tweets per day
    Author: Andrés Couble
    Date: June 3, 2022
    '''
    DF['Date'] = DF['created_at'].str[0:10]
    DF['Date'] = pd.to_datetime(DF['Date']).dt.date

    tweets_per_day = DF.groupby(['Date']).count()
    tweets_per_day['day'] = tweets_per_day.index
    
    plt.figure(figsize = (20, 10))
    plt.plot(tweets_per_day['day'], tweets_per_day['id'])
    #plt.axvline(dt.datetime(2021, 2, 10),linestyle = '--',color = 'red')
    #plt.axvline(dt.datetime(2021, 9, 26),linestyle = '--',color = 'green')
    #plt.axvline(dt.datetime(2022, 1, 29),linestyle = '--',color = 'green')
    plt.title('Tweets Per Day', fontsize = 18)
    plt.ylabel('Tweets Count', fontsize = 18)
    plt.xticks(rotation = 90, fontsize = 18)
    plt.yticks(fontsize = 18);


def pday_metrics(DF: pd.DataFrame, RT = True, Likes = True, Quotes = True, Reply = True):
    '''
    Objective: Plot retweets and/or likes and/or quotes and/or replies per tweet per day
    Author: Andrés Couble
    Date: June 3, 2022
    '''
    DF['Date'] = DF['created_at'].str[0:10]
    DF['Date'] = pd.to_datetime(DF['Date']).dt.date

    tweets_per_day = DF.groupby(['Date']).count()
    metrics_per_day = DF.groupby(['Date']).sum()

    graph = tweets_per_day[['id']].join(metrics_per_day[['public_metrics.like_count', 'public_metrics.quote_count',
       'public_metrics.reply_count', 'public_metrics.retweet_count']])
    
    graph['RT per tweet'] = graph['public_metrics.retweet_count']/graph['id']
    graph['Like per tweet'] = graph['public_metrics.like_count']/graph['id']
    graph['Reply per tweet'] = graph['public_metrics.reply_count']/graph['id']
    graph['Quote per tweet'] = graph['public_metrics.quote_count']/graph['id']
    graph['day'] = graph.index
    
    if RT == True:
        plt.figure(figsize = (20, 10))
        plt.plot(graph['day'], graph['RT per tweet'])
        plt.title('Retweets Per Tweet', fontsize = 18)
        plt.ylabel('Retweets Count', fontsize = 18)
        plt.xticks(rotation = 90, fontsize = 18)
        plt.yticks(fontsize = 18);
        plt.show();
        
    if Likes == True:
        plt.figure(figsize = (20, 10))
        plt.plot(graph['day'], graph['Like per tweet'])
        plt.title('Likes Per Tweet', fontsize = 18)
        plt.ylabel('Likes Count', fontsize = 18)
        plt.xticks(rotation = 90, fontsize = 18)
        plt.yticks(fontsize = 18);
        plt.show();
        
    if Quotes == True:
        sns.set()
        sns.set_theme(context = 'paper',style = 'whitegrid')
        plt.figure(figsize  =  (20, 10))
        plt.plot(graph['day'], graph['Quote per tweet'])
        plt.title('Quotes Per Tweet', fontsize = 18)
        plt.ylabel('Quotes Count', fontsize = 18)
        plt.xticks(rotation = 90, fontsize = 18)
        plt.yticks(fontsize = 18);
        plt.show();
        
    if Reply == True:
        sns.set()
        sns.set_theme(context = 'paper',style = 'whitegrid')
        plt.figure(figsize = (20, 10))
        plt.plot(graph['day'], graph['Reply per tweet'])
        plt.title('Replies Per Tweet', fontsize = 18)
        plt.ylabel('Replies Count', fontsize = 18)
        plt.xticks(rotation = 90, fontsize = 18)
        plt.yticks(fontsize = 18);
        plt.show();


def pday_hashtags(DF: pd.DataFrame, list_of_hashtags: list):
    '''
    Objective: Print the frequency of a list of hashtags per day
    Author: Andrés Couble
    Date: June 3, 2022
    '''
    df_1 = DF.copy()
    for hashtag in list_of_hashtags:
        df_hash = pd.DataFrame()
        df_hash = DF.dropna(subset = ['tweet_hashtags']).copy()
        df_hash = df_hash[df_hash.tweet_hashtags.str.contains(hashtag)]
        df_hash['count_' + str(hashtag)] = 1
        df_1 = df_1.merge(df_hash[['id','count_' + str(hashtag)]],how = "left",on = "id")
        
    df_1['Date'] = df_1['created_at'].str[0:10]
    df_1['Date'] = pd.to_datetime(df_1['Date']).dt.date
    metrics_per_day = df_1.groupby(['Date']).sum()
    
    fig, ax = plt.subplots(figsize = (18,8))
    for hashtag in list_of_hashtags:
        ax.plot(metrics_per_day['count_' + str(hashtag)], label = "#" + hashtag);
    ax.legend(loc = 'upper left', fontsize = 18);
    ax.set_title('Hashtags Frequency over Time', size = 18);
    ax.set_ylabel('Hashtags Count', size = 18);
    ax.tick_params(axis = "x", labelsize = 18);
    ax.tick_params(axis = "y", labelsize = 18);


def pday_word(DF: pd.DataFrame, list_of_words: list):
    '''
    Objective: Print the frequency of a list of words per day (one timeline for each word)
    Author: Andrés Couble
    Date: June 3, 2022
    '''
    df_1 = DF.copy()
    for word in list_of_words:
        regex = '(?:^|\W)' + word + '(?:$|\W)'
        df_hash = pd.DataFrame()
        df_hash = DF.dropna(subset = ['cleaned_text']).copy()
        df_hash = df_hash[df_hash.cleaned_text.str.contains(regex)]
        df_hash['count_' + str(word)] = 1
        df_1 = df_1.merge(df_hash[['id','count_' + str(word)]],how = "left",on = "id")
        
    df_1['Date'] = df_1['created_at'].str[0:10]
    df_1['Date'] = pd.to_datetime(df_1['Date']).dt.date
    metrics_per_day = df_1.groupby(['Date']).sum()
    
    fig, ax = plt.subplots(figsize = (18,8))
    for word in list_of_words:
        ax.plot(metrics_per_day['count_' + str(word)], label = word);
    ax.legend(loc = 'upper left', fontsize = 18);
    ax.set_title('Word Frequency over Time', size = 18);
    ax.set_ylabel('Word Count', size = 18);
    ax.tick_params(axis = "x", labelsize = 18);
    ax.tick_params(axis = "y", labelsize = 18);
    
    
def popular_tweets(DF: pd.DataFrame, metric = "Retweets", number = 10) -> str:
    '''
    Objective: Print the n most popular tweets by metric (Retweets, quotes or replies) with their associated metrics.
    Author: Andrés Couble
    Date: June 3, 2022
    '''
    if metric == "Likes":
        df_1 = DF.sort_values(by = ['public_metrics.like_count'],ascending = False)
        for i in range(0,number):
            print(df_1['text'].iloc[i])
            print("Author: " + str(df_1['author.username'].iloc[i]))
            print("RT: " + str(df_1['public_metrics.retweet_count'].iloc[i]))
            print("Likes: " + str(df_1['public_metrics.like_count'].iloc[i]))
            print("Quotes: " + str(df_1['public_metrics.quote_count'].iloc[i]))
            print("Replies: " + str(df_1['public_metrics.reply_count'].iloc[i]))
            print("")
    
    if metric == "Retweets":
        df_1 = DF.sort_values(by = ['public_metrics.retweet_count'],ascending = False)
        for i in range(0,number):
            print(df_1['text'].iloc[i])
            print("Author: " + str(df_1['author.username'].iloc[i]))
            print("RT: " + str(df_1['public_metrics.retweet_count'].iloc[i]))
            print("Likes: " + str(df_1['public_metrics.like_count'].iloc[i]))
            print("Quotes: " + str(df_1['public_metrics.quote_count'].iloc[i]))
            print("Replies: " + str(df_1['public_metrics.reply_count'].iloc[i]))
            print("")
    
    if metric == "Quotes":
        df_1 = DF.sort_values(by = ['public_metrics.quote_count'],ascending = False)
        for i in range(0,number):
            print(df_1['text'].iloc[i])
            print("Author: " + str(df_1['author.username'].iloc[i]))
            print("RT: " + str(df_1['public_metrics.retweet_count'].iloc[i]))
            print("Likes: " + str(df_1['public_metrics.like_count'].iloc[i]))
            print("Quotes: " + str(df_1['public_metrics.quote_count'].iloc[i]))
            print("Replies: " + str(df_1['public_metrics.reply_count'].iloc[i]))
            print("")
    
    if metric == "Replies":
        df_1 = DF.sort_values(by = ['public_metrics.reply_count'],ascending = False)
        for i in range(0,number):
            print(df_1['text'].iloc[i])
            print("Author: " + str(df_1['author.username'].iloc[i]))
            print("RT: " + str(df_1['public_metrics.retweet_count'].iloc[i]))
            print("Likes: " + str(df_1['public_metrics.like_count'].iloc[i]))
            print("Quotes: " + str(df_1['public_metrics.quote_count'].iloc[i]))
            print("Replies: " + str(df_1['public_metrics.reply_count'].iloc[i]))
            print("")

def compare_word_pday (DF,list_of_words,standarized=True):
    '''
    Objective: Print how many tweets (or the percentage per day) use words from a list.
    Author: Andrés Couble
    Date: June 10, 2022
    '''
    
    df_1=DF.copy()
    df_right=df_1[df_1['Label']=="Right"]
    df_left=df_1[df_1['Label']=="Left"]
    for word in list_of_words:
        regex = '(?:^|\W)'+word+'(?:$|\W)'
        df_word_right= df_right.dropna(subset=['cleaned_text']).copy()
        df_word_left=df_left.dropna(subset=['cleaned_text']).copy()

        df_word_right=df_word_right[df_word_right.cleaned_text.str.contains(regex)]
        df_word_left=df_word_left[df_word_left.cleaned_text.str.contains(regex)]
        
        df_word_right['count_'+str(word)]=1
        df_word_left['count_'+str(word)]=1
        
        df_right=df_right.merge(df_word_right[['id','count_'+str(word)]],how="left",on="id")
        df_left=df_left.merge(df_word_left[['id','count_'+str(word)]],how="left",on="id")
    
    df_right['total']=0
    df_left['total']=0
    
    title=str("")
    for word in list_of_words:
        df_right['count_'+str(word)]=df_right['count_'+str(word)].fillna(0)
        df_left['count_'+str(word)]=df_left['count_'+str(word)].fillna(0)
        
        df_right['total']+=df_right['count_'+str(word)]
        df_left['total']+=df_left['count_'+str(word)]
        title+=word+ " or "
        
    title=title[:-4]
    
    df_right['contains']=np.where(df_right.total>0,1,0)
    df_left['contains']=np.where(df_left.total>0,1,0)
           
        
    df_right['Date']=df_right['created_at'].str[0:10]
    df_left['Date']=df_left['created_at'].str[0:10]
    df_right['Date']=pd.to_datetime(df_right['Date']).dt.date
    df_left['Date']=pd.to_datetime(df_right['Date']).dt.date
    right_per_day=df_right.groupby(['Date']).sum()
    left_per_day=df_left.groupby(['Date']).sum()
    
    
    if standarized==False:
        fig, ax = plt.subplots(figsize=(18,8))
        ax.plot(right_per_day['contains'], label="Right frequency");
        ax.plot(left_per_day['contains'], label="Left frequency");
        ax.legend(loc='upper left');
        ax.set_title('Total Frequency of tweets that contains '+ title);
    
    if standarized==True:
        #Compute the total amount of tweets per day per affiliation to divide for it.
        total_right=df_right[['id','Date']].groupby(['Date']).count()
        total_left=df_left[['id','Date']].groupby(['Date']).count()
        total_right.rename(columns = {'id':'all_tweets'}, inplace = True)
        total_left.rename(columns = {'id':'all_tweets'}, inplace = True)
        right_per_day=right_per_day.join(total_right)
        left_per_day=left_per_day.join(total_left)
        
        right_per_day['proportion']=right_per_day['contains']/right_per_day['all_tweets']
        left_per_day['proportion']=left_per_day['contains']/left_per_day['all_tweets']
        
        fig, ax = plt.subplots(figsize=(18,8))
        ax.plot(right_per_day['proportion'], label="Right frequency");
        ax.plot(left_per_day['proportion'], label="Left frequency");
        ax.legend(loc='upper left');
        ax.set_title('Percentage of tweets that contains '+ title);