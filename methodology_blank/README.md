# `TxtAnLib` Documentation


## Functions to Filter Corpora
`f_authors(DF: pd.DataFrame, authors_list: list)`

Receive as input a list of authors and returns a data frame with the tweets from these authors.

**Parameters:**
* `DF`: Data frame to filter; Type: Pandas Dataframe
* `authors_list`: list of authors usernames to select the tweets from these users; Type: List of strings.

**Returns**: 
DataFrame with the same columns that the input DF, but considering only the tweets written by authors in the input list.

<br>
<br>

`f_dates(DF: pd.DataFrame, start_time, end_time)`

Receive as input a start time and end time and return the data frame only with the tweets tweeted
between these two dates.

**Parameters:**
* `DF`: Data frame to filter; Type: Pandas Dataframe
* `start_time`: Initial date of the period to filter; Type: String in format YYYY-MM-DD; Default: ”2020-
10-31”
* `end_time`: Final date of the period to filter; Type: String in format YYYY-MM-DD; Default: ”2022-
04-12”

**Returns:**
DataFrame with the same columns that the input DF, but considering only the tweets written
in the period between start time and end time.

<br>
<br>

`f_words(DF: pd.DataFrame, list_of_words: list)`

Receive a list of words and return a data
frame only with the tweets that contain one of these words

**Parameters:**
* `DF`: Data frame to filter; Type: Pandas Dataframe
* `list_of_words`: list of words to select the tweets that contains one of these words; Type: List of strings

**Returns:** 
DataFrame with the same columns that the input DF, but considering only the tweets that
contain at least one of the words in list of words.

<br>
<br>

`f_hashtags(DF: pd.DataFrame, list_of_hashtags: list)` 

Receive a list of hashtags and return
a data frame only with the tweets that contain one of these hashtags.

**Parameters:**
* `DF`: Data frame to filter; Type: Pandas Dataframe
* `list_of_hashtags`: list of authors words to select the tweets that contains one of these hashtags; Type: List of strings

**Returns:** 
DataFrame with the same columns that the input DF, but considering only the tweets that
contain at least one of the hashtags in list of hashtags.

<br>
<br>

`f_metrics(DF: pd.DataFrame, metric: str , threshold: int)` 

Filter tweets with a minimum number of RT, likes, quotes or resplies.

**Parameters:**
* `DF`: Data frame to filter; Type: Pandas Dataframe
* `metric`: Name of the metric that the user wants to use to filter. Options: ”Likes”, ”Retweets”, ”Quotes” or ”Replies”; Type: String
* `threshold`: Minimum number of the “metric” to filter tweets.

**Returns:**
DataFrame with the same columns that the input DF, but considering only the tweets that have more than the threshold number of the selected metric.


<br>
<br>

`f_location(DF: pd.DataFrame, list_of_locations: list)` 

Receive a list of words and return a data frame only with tweets from authors that have one of these words in the location.

**Parameters:**
* `DF`: Data frame to filter; Type: Pandas Dataframe
* `list_of_locations`: list of words to select the tweets from authors that contain at least one of these words in their self-written location; Type: List of strings

**Returns:** 
DataFrame with the same columns that the input DF, but considering only the tweets written by authors that contain in their location at least one of the words of the list of locations.

<br>
<br>

`f_affiliation(DF,Affiliation=”Unlabeled”)`

Receive an affiliation (Left, Right or Unlabeled) and return a DataFrame only with tweets from authors of this affiliation.

**Parameters:**
* `DF`: Data frame to filter; Type: Pandas Dataframe
* `Affiliation`: Affiliation to filter. Options: “Left”, “Right” or “Unlabeled”. Default:“Unlabeled”;Type: String.

**Returns:** 
DataFrame with the same columns that the input DF, but considering only the tweets written by authors of the selected affiliation

<br>
<br>

`f_verified(DF)` 

Return a Dataframe with tweets written by verified accounts.

**Parameters:**
* `DF`: Data frame to filter; Type: Pandas Dataframe

**Returns:**
DataFrame with the same columns that the input DF, but considering only the tweets written by verified accounts.

<br>
<br>

`f_minfollowers(DF,min_followers=200)`

Return a Dataframe with tweets written by accounts with a minimum number of followers.

**Parameters:**
* `DF`: Data frame to filter; Type: Pandas Dataframe
* `min_followers`: Minimum number of followers to filter the data frame. Default:200; Type:Int

**Returns:** 
DataFrame with the same columns that the input DF, but considering only the tweets written by accounts with more than min followers followers

<br>
<br>

## Functions to Visualize Corpora
`word_cloud(DF: pd.DataFrame, number_of_words = 100)`

Plot a Word Cloud of the input data set cleaned text.

**Parameters:**
* `DF`: Data frame with input data; Type: Pandas Dataframe
* `number_of_words`: Maximum number of words to display in the Word Cloud. Default: 100;Type: Int

**Returns:** 
None

**Action:**
Plot a Word Cloud of cleaned text from the DF.

<br>
<br>

`top_words(DF: pd.DataFrame, number_of_words = 100)`

Print the n most used words in the Data Frame and the number of occurrences.

**Parameters:**
* `DF`: Data frame with input data; Type: Pandas Dataframe
* `number_of_words`: Number of most used words to display. Default: 100;Type: Int

**Return:**
List of n tuples with the most used words and the number of occurrences.

**Action:**
Print the n most used words and the number of occurrences.

<br>
<br>

`top_authors(DF: pd.DataFrame, number_of_authors = 100)`

Print n authors username that tweets more often in the DF.

**Parameters:**
* `DF`: Data frame with input data; Type: Pandas Dataframe
* `number_of_authors`: Number of most common authors to display. Default: 100;Type: Int

**Return:**
List of n tuples with the n authors that tweet most often in DF and the number of tweets
that each one has.

**Action:**
Print the n authors that tweeted more and the number of tweets for each one.

<br>
<br>

`top_hashtags(DF: pd.DataFrame, number_print=100, number_plot=20, title = ’ ’)`

Print the n print most used hashtags in the Data Frame and the number of occurrences. Also plot a bar plot with the n plot top hashtags.

**Parameters:**
* `DF`: Data frame with input data; Type: Pandas Dataframe
* `number_print`: Number of most used hashtags to print. Default:100;Type:int. number_plot: Number of most used hashtags to include in the bar plot. Default:20;Type:int. title: Title for the bar plot. Default:” “; Type: String.

**Return:** 
List of n print tuples with the n most used hashtags and the number of occurrences.

**Action:**
Print the n print most used hashtags in the Data Frame and the number of occurrences. Also display a bar plot with the n plot number of most used hashtags. Each bar represent the number of occurrences.

<br>
<br>

`top_bigrams(DF:pd.DataFrame, number_of_bigrams=100, number_plot=20, title = ””, split_bi = False)`

Print the n print most used bigrams in the Data Frame and the number of occurrences. Also plot a bar plot with the n plot top bigrams.

**Parameters:**
* `DF`: Data frame with input data; Type: Pandas Dataframe
* `number_of_bigrams`: Number of most used bigrams to print. Default:100;Type:int. 
* `number_plot`: Number of most used bigrams to include in the bar plot. Default:20;Type:int. title: Title for the bar plot. Default:”“; Type: String.
* `split_bi`: Boolean to indicate if in the labels of the bar plot the bigrams are presented in two lines (True) or in one line (False). Default: False; Type: Boolean

**Return:**
List of n print tuples with the n most used bigrams and the number of occurrences.

**Action:**
Print the n print most used bigrams in the Data Frame and the number of occurrences. Also display a bar plot with the n plot number of most used bigrams. Each bar represent the number of occurrences.

<br>
<br>

`pday_tweets(DF: pd.DataFrame)`

Print a time series indicating the number of tweets per day.

**Parameters:**
* `DF`: Data frame with input data; Type: Pandas Dataframe

**Return:**
None

**Action:**
Display time series plot indicating the number of tweets per day.

<br>
<br>

`pday_metrics(DF: pd.DataFrame, RT = True, Likes = True, Quotes = True, Reply = True)`

Print time series for each indicated metric with the number of these metrics per tweet for each day.

**Parameters:**
* `DF`: Data frame with input data; Type: Pandas Dataframe
* `RT`: If True, display the time series of retweets per tweet. Default: True; Type: Boolean
* `Likes`: If True, display the time series of likes per tweet. Default: True; Type: Boolean
* `Quotes`: If True, display the time series of quotes per tweet. Default: True; Type: Boolean
* `Reply`: If True, display the time series of replies per tweet. Default: True; Type: Boolean

**Return:**
None

**Action:**
Display time series plots indicating the number of the selected metrics per tweet for each day



<br>
<br>

`pday_hashtags(DF: pd.DataFrame, list_of_hashtags: list)`

Plot one time series for each hashtag in the list, showing the number of tweets per day that contain the hashtags. All the time series are displayed together in the same plot.

**Parameters:**
* `DF`: Data frame with input data; Type: Pandas Dataframe
* `list_of_hashtags`: List of hashtags that the user wants to see the time series; Type: List of strings. It is not necessary to include the # before the hashtag.

**Return:** 
None

**Action:**
Display time series plot showing the number of tweets that contains each of the hashtags in the list.



<br>
<br>

`pday_word(DF: pd.DataFrame, list_of_words: list)`

Plot one time series for each word in the list, showing the number of tweets per day that contain the word. All the time series are displayed together in the same plot.

**Parameters:**
* `DF`: Data frame with input data; Type: Pandas Dataframe
* `list_of_words`: List of words that the user wants to see the time series; Type: List of strings.

**Return:**
None

**Action:**
Display time series plot showing the number of tweets that contains each of the words in the list.


<br>
<br>

`popular_tweets(DF: pd.DataFrame, metric = ”Retweets”, number = 10)`

Print the n most popular tweets. Popularity is measured as the tweets with the highest number of reactions of the selected metric.

**Parameters:**
* `DF`: Data frame with input data; Type: Pandas Dataframe 
* `metric`: Name of the metric that the user wants to use to filter. Options: ”Likes”, ”Retweets”, ”Quotes” or ”Replies”. Default: ”Retweets”; Type: String
* `Number`: Number of tweets to print. Default: 10; Type: Int

**Return:**
None

**Action:**
Print the n tweets most popular according to the selected metric.

<br>
<br>

`compare_word_pday(DF, list_of_words, standarized=True)`

Plot time series with the number (or proportion) of tweets per day that contain at least one of the words of the list for right leaning and left leaning people. Both time series are displayed in the same plot to compare.

**Parameters:**
* `DF`: Data frame with input data; Type: Pandas Dataframe list of words: List of words that the user wants to see their use on time for right and left leaning people. Type: List of strings 
* `standardized`: If True, display the proportion of tweets that contain the words per day, if it is False, display the total number of tweets that contain these words. Default: True; Type: Boolean.

**Return:**
None

**Action:**
Time series with the use of the selected words over time for left- and right-wing users.



