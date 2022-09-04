import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt
#import seaborn as sns
import re
#import warnings
#import random
import unidecode
import emoji
import textwrap
from wordcloud import WordCloud
from nltk.corpus import stopwords

#from datetime import datetime



def regex_chile(df: pd.DataFrame, col, colname: str) -> pd.DataFrame:
    '''
    Objective: Function to match ':Chile:' regular expression and reorder columns
    Author: Mathias Schindler
    Date: May 24, 2022
    '''
    df[colname] = df[col].str.match(r'((.*?):Chile:(.*?))')
    _ = df.columns.to_list()
    cols_neworder = _[0:2] + [_[5]] + [_[40]] + [_[46]] + _[74:76]
    df_out = df[cols_neworder]
    
    return df_out


def tweets_preproz(df: pd.Series, drop_na: bool, drop_dup: bool) -> pd.DataFrame:
    '''
    Objective: Function to preprocess twarc-df cols
    Author: Mathias Schindler
    Date: May 24, 2022
    '''
    # Convert to string
    df = df.astype("string")

    # Lowercase strings
    df = df.str.lower()

    # Remove/fill NaNs
    if drop_na == True:
        df = df.dropna()
    elif drop_na == False:
        df = df.fillna("0")
    else:
        pass

    # Unidecode Spanish letters (e.g. á, ó, ñ, ...)
    df = df.apply(unidecode.unidecode)
    
    # Drop duplicates (or not)
    if drop_dup == True:
        df = df.drop_duplicates()
    elif drop_dup == False:
        pass
    else:
        pass
    
    return df


def make_other_country_df(old_cols: list, prefix: str, df_in: pd.DataFrame, bool_col_name, col_new_name: str) -> pd.DataFrame:
    '''
    Objective: Function for Section 1.3; Making dataframes with other country indicators
    Author: Mathias Schindler
    Date: May 24, 2022
    '''
    # Add prefix to columns
    pref = prefix
    new_cols_pref = [pref + k for k in old_cols]  #['id', 'conversation_id', 'author_id'] + 
    cols_dict_pref = {old_cols[i]: new_cols_pref[i] for i in range(len(old_cols))}
    df_in = df_in.rename(columns = cols_dict_pref)

    # Reorder columns
    _ = df_in.columns.to_list()
    new_col_order = ['id', 'conversation_id', 'author_id'] + _[74:]
    df_in = df_in[new_col_order]

    # Boolean column if any other country and SAVE
    bool_col_name = df_in.iloc[:, 3:].any(axis = 1)

    # Concat into final auxiliary df
    df_out = pd.concat([df_in, bool_col_name], axis = 1)
    df_out = df_out.rename(columns = {0:col_new_name})
    _ = df_out.columns.to_list()
    new_list = _[:3] + [col_new_name] + _[3:-1]
    df_out = df_out[new_list]
    
    return df_out


def dict_regex_city(df_out_prefix: str, df_in: pd.DataFrame, col, regex: str, city) -> pd.DataFrame:
    '''
    Objective: Function to save different dataframes with different names
    Author: Mathias Schindler
    Date: May 24, 2022
    '''
    # Make df prefix
    df_prefix = df_out_prefix + '_%s'
    
    # RegEx: Containing other country than Chile
    globals()[df_prefix % city] = df_in[col][df_in[col].str.match(regex) == True]

    # Convert to df
    globals()[df_prefix % city] = globals()[df_prefix % city].to_frame()

    # Add boolean column
    globals()[df_prefix % city][city] = True

    # Remove other column
    globals()[df_prefix % city] = globals()[df_prefix % city].drop(col, axis = 1)
    
    # Give name to pd.DataFrame
    globals()[df_prefix % city].name = str(city)
                                            
    return globals()[df_prefix % city]


def city_dict_df(prefix: str, old_cols: list, df_in: pd.DataFrame, bool_col_name, col_new_name: str) -> pd.DataFrame:
    '''
    Objective: For Section 1.4; Renaming columns and creating a boolean column
    Author: Mathias Schindler
    Date: May 24, 2022
    '''
    # Add prefix to columns
    pref = prefix
    new_cols_pref = [pref + k for k in old_cols]
    cols_dict_pref = {old_cols[i]: new_cols_pref[i] for i in range(len(old_cols))}
    df_in = df_in.rename(columns = cols_dict_pref)

    # Reorder columns
    _ = df_in.columns.to_list()
    new_col_order = ['id', 'conversation_id', 'author_id'] + _[74:]
    df_in = df_in[new_col_order]

    # Boolean column if any city
    bool_col_name = df_in.iloc[:, 3:].any(axis = 1)

    # Concat into final auxiliary df
    df_out = pd.concat([df_in, bool_col_name], axis = 1)
    df_out = df_out.rename(columns = {0: col_new_name})
    _ = df_out.columns.to_list()
    new_list = _[:3] + [col_new_name] + _[3:-1]
    df_out = df_out[new_list]

    return df_out


def fix_na_loc_bio(df1: pd.Series, df2: pd.Series) -> pd.DataFrame:
    '''
    Objective: For Section 3; Imputing NaN col values between same cols in two dataframes
    Author: Mathias Schindler
    Date: May 24, 2022
    '''
    df1 = np.where(df1.isnull(), df2, df1)
    
    return df1


def cleanTweets(s: str, remove_hash: bool) -> str:
    '''
    Objective: Custom function to clean tweets
    Author: Luis Menéndez, Universitat Autonoma de Barcelona
    Date: Unknown
    '''
    stopwords_eng =stopwords.words("english")
    stopwords_es =stopwords.words("spanish")
    stopwords_all=stopwords_eng+stopwords_es

    # Function to clean tweets, for now i am keeping emojis and hashtags. Alternative version
    if type(s)==np.float64:
        return ""
    #Demojize text
#    s=emoji.demojize(s,delimiters=("", " "))
    
    # Remove new lines, etc.
    s = s.replace(r'<lb>', "\n")
    s = s.replace(r'<tab>', "\i")
    s = re.sub(r'<br */*>', "\n", s)
    s = s.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&")
    s = s.replace("&amp;", "&")
    s = s.replace("\n", " ")
    s = s.replace("\\n", " ")
    
#    emoji_pattern = re.compile("["
#        u"\U0001F600-\U0001F64F"  # emoticons
#        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
#        u"\U0001F680-\U0001F6FF"  # transport & map symbols
#        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
#                           "]+", flags=re.UNICODE)
#    s= emoji_pattern.sub(r'', s)
    
    # Markdown urls
    s = re.sub(r'\(https*://[^\)]*\)', "", s)
    
    # Normal urls
    s = re.sub(r'https*://[^\s]*', "", s)
    #s = re.sub(r'_+', ' ', s)
    s = re.sub(r'"+', '"', s)
    
    # Remove punctuation    
    s = re.sub('[()!?]', ' ', s)
    s = re.sub('\[.*?\]',' ', s)
    s = re.sub('\[,*?\]',' ', s)
    
    # Custom removals
    #s = re.sub(r'@[A-Za-z0-9_]+', "", s) # replace mentions
    #s = re.sub(r':[^:]+','[emoji]',s) # remove demojized text
    s= re.sub(r'[0-9]','',s)# remove digits
    
    s = s.translate(str.maketrans('', '', '!"$%&\'()*+,-./:;<=>?[\\]^_`{|}~'))
    
    s = s.lower()
    if remove_hash == True:
        s = re.sub(r'#[A-Za-z0-9_]+', "", s)
    
    # Remove stopwords
    s = ' '.join([word for word in s.split() if word not in stopwords_all])
    
    return str(s)


def wordcloud_preproz(df: pd.DataFrame, col: str, hash_rm: bool) -> pd.DataFrame:
    '''
    Objective: Prepare pd.Series into one long string to be used for WordCloud visualization
    Requires: Luis' custom function to clean tweets (above)
    Author: Mathias Schindler
    Date: May 24, 2022
    '''
    # For wordcloud all 'author.description' rows should be made into one long string 
    out1 = df[col]
    out1 = out1.astype('string').fillna('0')

    # Make into one string
    out2 = " ".join(i for i in out1)

    # Unidecode, remove á, ó, ñ, etc.
    out2 = unidecode.unidecode(out2)

    # Luis' custom "cleanTweets()" function
    out2 = cleanTweets(s = out2, remove_hash = hash_rm)
    
    return out2