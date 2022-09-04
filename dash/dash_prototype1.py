###################################################################
#
# GUIDE TO RUN
# 1) Find venv path: E.g. (for me) /Users/mathiasschindler/opt/anaconda3/envs/thesis_pip
#
# 2) Find python path in venv: E.g. (for me) /Users/mathiasschindler/opt/anaconda3/envs/thesis_pip/bin/python
#
# 3) 'cd' terminal into directory where dash .py-file is located. E.g. (for me) /Users/mathiasschindler/Library/Mobile Documents/com~apple~CloudDocs/BSE/~~Git-repo-clones/ChileGov/dash
#
# 4) Run command in terminal: /Users/mathiasschindler/opt/anaconda3/envs/thesis_pip/bin/python dash_attempt5.py
#
# 5) Open in browser of choice hosted link provided by dash in terminal. E.g. (for me) 'Dash is running on http://127.0.0.1:8050/'
# 
# 6) Dash interface will update in real-time as changes are made to .py-file
#
###################################################################


# Imports
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px

import pandas as pd
import numpy as np
from datetime import date
from collections import Counter
import random

from TxtAnLib.filtering import filters
from TxtAnLib.visualizers import viz

# Set path + separator
path = "/Users/mathiasschindler/Library/Mobile Documents/com~apple~CloudDocs/BSE/_T3--Thesis/data_in"
out_path = '/Users/mathiasschindler/Library/Mobile Documents/com~apple~CloudDocs/BSE/_T3--Thesis/data_out'
sep = "/"

# Load data
df = pd.read_csv(path + sep + "Final_Labeled_Data_Set.csv", index_col = 0)
df = df.drop(df.columns.difference(['id', 'created_at', 'Label', 'tweet_hashtags', 'author.username', 'cleaned_text']), axis = 1)

df['Date'] = df['created_at'].str[0:10]
#df['Date'] = pd.to_datetime(df['Date']).dt.date
df['Date'] = pd.to_datetime(df['Date'])


# Instantiate app
app = dash.Dash(__name__)
app.title = 'Online Polarization in Chile'


# Describe app UI
app.layout = html.Div(children = [html.H1('Online Polarization in Developing Countries'),
                                  html.H3('NB: Note Graphs Can Have Different Y-Axis Scales'),
                                  html.I('Choose a Metric from Drop-Down Below to be Displayed:'),
                                  dcc.Dropdown(id = 'fig_choice', 
                                               options = [{'label':'Daily Tweet Count', 'value':'Daily Tweet Count'}, 
                                                          {'label':'Hashtags', 'value':'Hashtags'},
                                                          {'label':'Top Authors', 'value':'Top Authors'},
                                                          {'label':'Words', 'value':'Words'}],
                                               #value = 'Daily Tweet Count'),
                                               ),
                                  html.Br(), html.Br(),
                                  html.I('Choose a Date Range from Below to be Displayed:'),
                                  html.Br(),
                                  dcc.DatePickerRange(
                                      id = 'date_pick',
                                      min_date_allowed = date(2020, 11, 1),
                                      max_date_allowed = date(2022, 4, 10),
                                      initial_visible_month = date(2020, 11, 1),
                                      start_date = date(2020, 11, 1),
                                      end_date = date(2022, 4, 10)
                                  ),
                                  html.H2('For Total Corpus:'),
                                  html.Div(dcc.Graph(id = 'fig_tot')
                                  ),
                                  html.H2('By Political Affiliation:'),
                                  html.Div(children = [dcc.Graph(id = 'fig_lef', style = {'display': 'inline-block', 'width': '50%', 'height': '100%'}),
                                                       dcc.Graph(id = 'fig_rig', style = {'display': 'inline-block', 'width': '50%', 'height': '100%'})
                                  ]),
                                  html.H2('Random Tweet:'),
                                  #html.Br(),
                                  html.Button('Random Tweet – Full Corpus', id = 'r_tweet_fullc'),
                                  html.Br(), html.Br(),
                                  html.I(id = 'r_tweet_fullc_out', style = {'font_size': '32px'}),
                                  html.Div(id = 'r_auth_fullc_out', style={'marginBottom': '5em'}),
                                  
                                  html.Button('Random Tweet – Left-Leaning Users', id = 'r_tweet_lef'),
                                  html.Br(), html.Br(),
                                  html.I(id = 'r_tweet_lef_out', style = {'font_size': '32px'}),
                                  html.Div(id = 'r_auth_lef_out', style={'marginBottom': '5em'}),
                                  
                                  html.Button('Random Tweet – Right-Leaning Users', id = 'r_tweet_rig'),
                                  html.Br(), html.Br(),
                                  html.I(id = 'r_tweet_rig_out', style = {'font_size': '32px'}),
                                  html.Div(id = 'r_auth_rig_out', style={'marginBottom': '30em'})
                                 ]
                     )



# Callbacks

# Callback for random tweets – Full corpus
@app.callback(
    Output('r_tweet_fullc_out', 'children'),
    Input('r_tweet_fullc', 'n_clicks'),
    Input('date_pick', 'start_date'),
    Input('date_pick', 'end_date')
)
def update_output(n_clicks, start_date, end_date):
    if n_clicks == None:
        string = 'Press button above to show a random tweet from full corpus'
        
    else:
        df_tot = df.copy()
        df_tot = df_tot[['Date', 'author.username', 'cleaned_text']]
        df_tot = df_tot[(df_tot['Date'] >= start_date) & (df_tot['Date'] <= end_date)]
        
        n = random.randint(0, len(df_tot))
        string_auth = df_tot['author.username'].iloc[n]
        string_twee = '"' + df_tot['cleaned_text'].iloc[n] + '"'
        string = string_twee
        
    return string

@app.callback(
    Output('r_auth_fullc_out', 'children'),
    Input('r_tweet_fullc', 'n_clicks'),
    Input('date_pick', 'start_date'),
    Input('date_pick', 'end_date')
)
def update_output(n_clicks, start_date, end_date):
    if n_clicks == None:
        string = ' '
        
    else: 
        df_tot = df.copy()
        df_tot = df_tot[['Date', 'author.username', 'cleaned_text']]
        df_tot = df_tot[(df_tot['Date'] >= start_date) & (df_tot['Date'] <= end_date)]
        
        n = random.randint(0, len(df_tot))
        string_auth = df_tot['author.username'].iloc[n]
        string_twee = '"' + df_tot['cleaned_text'].iloc[n] + '"'
        string = 'Author: @' + string_auth
        
    return string

# Callback for random tweets – left corpus
@app.callback(
    Output('r_tweet_lef_out', 'children'),
    Input('r_tweet_lef', 'n_clicks'),
    Input('date_pick', 'start_date'),
    Input('date_pick', 'end_date')
)
def update_output(n_clicks, start_date, end_date):
    if n_clicks == None:
        string = 'Press button above to show a random tweet from corpus of left-leaning Chilean Twitter userse'
        
    else: 
        df_lef = df.copy(deep = True)
        df_lef = filters.f_affiliation(df, 'Left')
        df_lef = df_lef[['Date', 'author.username', 'cleaned_text']]
        df_lef = df_lef[(df_lef['Date'] >= start_date) & (df_lef['Date'] <= end_date)]
        
        n = random.randint(0, len(df_lef))
        string_auth = df_lef['author.username'].iloc[n]
        string_twee = '"' + df_lef['cleaned_text'].iloc[n] + '"'
        string = string_twee
        
    return string

@app.callback(
    Output('r_auth_lef_out', 'children'),
    Input('r_tweet_lef', 'n_clicks'),
    Input('date_pick', 'start_date'),
    Input('date_pick', 'end_date')
)
def update_output(n_clicks, start_date, end_date):
    if n_clicks == None:
        string = ' '
        
    else: 
        df_lef = df.copy(deep = True)
        df_lef = filters.f_affiliation(df, 'Left')
        df_lef = df_lef[['Date', 'author.username', 'cleaned_text']]
        df_lef = df_lef[(df_lef['Date'] >= start_date) & (df_lef['Date'] <= end_date)]
        
        n = random.randint(0, len(df_lef))
        string_auth = df_lef['author.username'].iloc[n]
        string_twee = '"' + df_lef['cleaned_text'].iloc[n] + '"'
        string = 'Author: @' + string_auth
        
    return string

# Callback for random tweets – right corpus
@app.callback(
    Output('r_tweet_rig_out', 'children'),
    Input('r_tweet_rig', 'n_clicks'),
    Input('date_pick', 'start_date'),
    Input('date_pick', 'end_date')
)
def update_output(n_clicks, start_date, end_date):
    if n_clicks == None:
        string = 'Press button above to show a random tweet from corpus of right-leaning Chilean Twitter userse'
        
    else: 
        df_rig = df.copy(deep = True)
        df_rig = filters.f_affiliation(df, 'Right')
        df_rig = df_rig[['Date', 'author.username', 'cleaned_text']]
        df_rig = df_rig[(df_rig['Date'] >= start_date) & (df_rig['Date'] <= end_date)]
        
        n = random.randint(0, len(df_rig))
        string_auth = df_rig['author.username'].iloc[n]
        string_twee = '"' + df_rig['cleaned_text'].iloc[n] + '"'
        string = string_twee
        
    return string

@app.callback(
    Output('r_auth_rig_out', 'children'),
    Input('r_tweet_rig', 'n_clicks'),
    Input('date_pick', 'start_date'),
    Input('date_pick', 'end_date')
)
def update_output(n_clicks, start_date, end_date):
    if n_clicks == None:
        string = ' '
        
    else: 
        df_rig = df.copy(deep = True)
        df_rig = filters.f_affiliation(df, 'Right')
        df_rig = df_rig[['Date', 'author.username', 'cleaned_text']]
        df_rig = df_rig[(df_rig['Date'] >= start_date) & (df_rig['Date'] <= end_date)]
        
        n = random.randint(0, len(df_rig))
        string_auth = df_rig['author.username'].iloc[n]
        string_twee = '"' + df_rig['cleaned_text'].iloc[n] + '"'
        string = 'Author: @' + string_auth
        
    return string


# Callback for left-leaning figure
@app.callback(Output(component_id = 'fig_lef',
                     component_property = 'figure'), 
              Input(component_id = 'fig_choice',
                    component_property = 'value'),
              Input('date_pick', 'start_date'),
              Input('date_pick', 'end_date')
              )
def update_plot_lef(input_metric, start_date, end_date):
    if input_metric == None:
        plot = px.bar()
    
    elif input_metric == 'Hashtags':
        df_lef = df.copy(deep = True)
        df_lef = filters.f_affiliation(df, 'Left')
        
        df_lef = df_lef[(df_lef['Date'] >= start_date) & (df_lef['Date'] <= end_date)]
        
        hasht = []
        n = 20
        for i in df_lef.index:
            try:
                hasht.append(df_lef['tweet_hashtags'][i].split(","))
            except:
                hasht.append([])

        df_lef['list_hashtags'] = hasht
        hashtags = []
        for ix in df_lef.index:
            hashtags += df_lef['list_hashtags'][ix]
        count = Counter(hashtags)
        most_occur = count.most_common(n)
        data = most_occur[0:n]

        n_groups = len(data)

        vals = [x[1] for x in data]
        legends = [x[0] for x in data]
        legends = ['#' + hashtag for hashtag in legends]

        index = np.arange(n_groups)
        
        df_bar = pd.DataFrame({'hashtag': legends, 'count':vals})
        
        plot = px.bar(data_frame = df_bar, 
                         x = 'hashtag', 
                         y = 'count', 
                         title = 'Top 20 Hashtags for Left-Leaning Chilean Twitter Users')
        plot.update_traces(marker_color = 'crimson')

    elif input_metric == 'Daily Tweet Count':
        df_lef = df.copy(deep = True)
        df_lef = filters.f_affiliation(df, 'Left')
        
        df_lef = df_lef[(df_lef['Date'] >= start_date) & (df_lef['Date'] <= end_date)]
        
        tweets_per_day = df_lef.groupby(['Date']).count()
        tweets_per_day['day'] = tweets_per_day.index
        tweets_per_day = tweets_per_day.rename(columns={'id':'count'})
        
        plot = px.line(data_frame = tweets_per_day, 
                   x = 'day', 
                   y = 'count', 
                   title = 'Tweets per Day for Left-Leaning Chilean Twitter Users')
        plot.update_traces(line_color = 'crimson')
        
    elif input_metric == 'Top Authors':
        df_lef = df.copy(deep = True)
        df_lef = filters.f_affiliation(df, 'Left')
        
        df_lef = df_lef[(df_lef['Date'] >= start_date) & (df_lef['Date'] <= end_date)]
        
        count = Counter(list(df_lef['author.username']))
        most_occur = count.most_common(20)
        data = most_occur[0:21]

        n_groups = len(data)

        vals = [x[1] for x in data]
        legends = [x[0] for x in data]
        legends = ['@' + hashtag for hashtag in legends]
        
        index = np.arange(n_groups)
        
        df_bar = pd.DataFrame({'author': legends, 'count':vals})
        
        plot = px.bar(data_frame = df_bar, 
                         x = 'author', 
                         y = 'count', 
                         title = 'Top 20 Authors for Left-Leaning Chilean Twitter Users')
        plot.update_traces(marker_color = 'crimson')
        
    elif input_metric == 'Words':
        df_lef = df.copy(deep = True)
        df_lef = filters.f_affiliation(df, 'Left')
        
        df_lef = df_lef[(df_lef['Date'] >= start_date) & (df_lef['Date'] <= end_date)]

        string = " ".join(list(df_lef['cleaned_text'].astype(str)))
        split_it = string.split()
        counter = Counter(split_it)
        most_occur = counter.most_common(20)
        data = most_occur[0:21]

        n_groups = len(data)

        vals = [x[1] for x in data]
        legends = [x[0] for x in data]
        
        index = np.arange(n_groups)
        
        df_bar = pd.DataFrame({'word': legends, 'count':vals})
        
        plot = px.bar(data_frame = df_bar, 
                         x = 'word', 
                         y = 'count', 
                         title = 'Top 20 Words for Left-Leaning Chilean Twitter Users')
        plot.update_traces(marker_color = 'crimson')
        
        
    return plot


# Callback for right-leaning figure
@app.callback(Output(component_id = 'fig_rig',
                     component_property = 'figure'), 
              Input(component_id = 'fig_choice',
                    component_property = 'value'),
              Input('date_pick', 'start_date'),
              Input('date_pick', 'end_date')
              )
def update_plot_rig(input_metric, start_date, end_date):
    if input_metric == None:
        plot = px.bar()
    
    elif input_metric == 'Hashtags':
        df_rig = df.copy(deep = True)
        df_rig = filters.f_affiliation(df, 'Right')
        
        df_rig = df_rig[(df_rig['Date'] >= start_date) & (df_rig['Date'] <= end_date)]
        
        hasht = []
        n = 20
        for i in df_rig.index:
            try:
                hasht.append(df_rig['tweet_hashtags'][i].split(","))
            except:
                hasht.append([])

        df_rig['list_hashtags'] = hasht
        hashtags = []
        for ix in df_rig.index:
            hashtags += df_rig['list_hashtags'][ix]
        count = Counter(hashtags)
        most_occur = count.most_common(n)
        data = most_occur[0:n]

        n_groups = len(data)

        vals = [x[1] for x in data]
        legends = [x[0] for x in data]
        legends = ['#' + hashtag for hashtag in legends]

        index = np.arange(n_groups)
        
        df_bar = pd.DataFrame({'hashtag': legends, 'count':vals})
        
        plot = px.bar(data_frame = df_bar, 
                         x = 'hashtag', 
                         y = 'count', 
                         title = 'Top 20 Hashtags for Right-Leaning Chilean Twitter Users')
        plot.update_traces(marker_color = 'orange')

    elif input_metric == 'Daily Tweet Count':
        df_rig = df.copy(deep = True)
        df_rig = filters.f_affiliation(df, 'Right')
        
        df_rig = df_rig[(df_rig['Date'] >= start_date) & (df_rig['Date'] <= end_date)]
        
        tweets_per_day = df_rig.groupby(['Date']).count()
        tweets_per_day['day'] = tweets_per_day.index
        tweets_per_day = tweets_per_day.rename(columns={'id':'count'})
        
        plot = px.line(data_frame = tweets_per_day, 
                   x = 'day', 
                   y = 'count', 
                   title = 'Tweets per Day for Right-Leaning Chilean Twitter Users')
        plot.update_traces(line_color = 'orange')
        
    elif input_metric == 'Top Authors':
        df_rig = df.copy(deep = True)
        df_rig = filters.f_affiliation(df, 'Right')
        
        df_rig = df_rig[(df_rig['Date'] >= start_date) & (df_rig['Date'] <= end_date)]
        
        count = Counter(list(df_rig['author.username']))
        most_occur = count.most_common(20)
        data = most_occur[0:21]

        n_groups = len(data)

        vals = [x[1] for x in data]
        legends = [x[0] for x in data]
        legends = ['@' + hashtag for hashtag in legends]
        
        index = np.arange(n_groups)
        
        df_bar = pd.DataFrame({'author': legends, 'count':vals})
        
        plot = px.bar(data_frame = df_bar, 
                         x = 'author', 
                         y = 'count', 
                         title = 'Top 20 Authors for Right-Leaning Chilean Twitter Users')
        plot.update_traces(marker_color = 'orange')
        
    elif input_metric == 'Words':
        df_rig = df.copy(deep = True)
        df_rig = filters.f_affiliation(df, 'Right')
        
        df_rig = df_rig[(df_rig['Date'] >= start_date) & (df_rig['Date'] <= end_date)]

        string = " ".join(list(df_rig['cleaned_text'].astype(str)))
        split_it = string.split()
        counter = Counter(split_it)
        most_occur = counter.most_common(20)
        data = most_occur[0:21]

        n_groups = len(data)

        vals = [x[1] for x in data]
        legends = [x[0] for x in data]
        
        index = np.arange(n_groups)
        
        df_bar = pd.DataFrame({'word': legends, 'count':vals})
        
        plot = px.bar(data_frame = df_bar, 
                         x = 'word', 
                         y = 'count', 
                         title = 'Top 20 Words for Right-Leaning Chilean Twitter Users')
        plot.update_traces(marker_color = 'orange')
        
    return plot


# Callback for total corpus figure
@app.callback(Output(component_id = 'fig_tot',
                     component_property = 'figure'), 
              Input(component_id = 'fig_choice',
                    component_property = 'value'),
              Input('date_pick', 'start_date'),
              Input('date_pick', 'end_date')
              )
def update_plot_rig(input_metric, start_date, end_date):
    if input_metric == None:
        plot = px.bar()
    
    elif input_metric == 'Hashtags':
        df_tot = df.copy()
        df_tot = df_tot[(df_tot['Date'] >= start_date) & (df_tot['Date'] <= end_date)]
        
        hasht = []
        n = 20
        for i in df_tot.index:
            try:
                hasht.append(df_tot['tweet_hashtags'][i].split(","))
            except:
                hasht.append([])

        df_tot['list_hashtags'] = hasht
        hashtags = []
        for ix in df.index:
            hashtags += df_tot['list_hashtags'][ix]
        count = Counter(hashtags)
        most_occur = count.most_common(n)
        data = most_occur[0:n]

        n_groups = len(data)

        vals = [x[1] for x in data]
        legends = [x[0] for x in data]
        legends = ['#' + hashtag for hashtag in legends]

        index = np.arange(n_groups)
        
        df_bar = pd.DataFrame({'hashtag': legends, 'count':vals})
        
        plot = px.bar(data_frame = df_bar, 
                         x = 'hashtag', 
                         y = 'count', 
                         title = 'Top 20 Hashtags for Total Corpus of Chilean Twitter Users')
        plot.update_traces(marker_color = 'blue')

    elif input_metric == 'Daily Tweet Count':
        df_tot = df.copy()
        df_tot = df_tot[(df_tot['Date'] >= start_date) & (df_tot['Date'] <= end_date)]
        
        tweets_per_day = df_tot.groupby(['Date']).count()
        tweets_per_day['day'] = tweets_per_day.index
        tweets_per_day = tweets_per_day.rename(columns={'id':'count'})
        
        plot = px.line(data_frame = tweets_per_day, 
                   x = 'day', 
                   y = 'count', 
                   title = 'Tweets per Day for Total Corpus of Chilean Twitter Users')
        plot.update_traces(line_color = 'blue')
        
    elif input_metric == 'Top Authors':
        df_tot = df.copy()
        df_tot = df_tot[(df_tot['Date'] >= start_date) & (df_tot['Date'] <= end_date)]
        
        count = Counter(list(df_tot['author.username']))
        most_occur = count.most_common(20)
        data = most_occur[0:21]

        n_groups = len(data)

        vals = [x[1] for x in data]
        legends = [x[0] for x in data]
        legends = ['@' + hashtag for hashtag in legends]
        
        index = np.arange(n_groups)
        
        df_bar = pd.DataFrame({'author': legends, 'count':vals})
        
        plot = px.bar(data_frame = df_bar, 
                         x = 'author', 
                         y = 'count', 
                         title = 'Top 20 Authors for Total Corpus of Chilean Twitter Users')
        plot.update_traces(marker_color = 'blue')
        
    elif input_metric == 'Words':
        df_tot = df.copy()
        df_tot = df_tot[(df_tot['Date'] >= start_date) & (df_tot['Date'] <= end_date)]

        string = " ".join(list(df_tot['cleaned_text'].astype(str)))
        split_it = string.split()
        counter = Counter(split_it)
        most_occur = counter.most_common(20)
        data = most_occur[0:21]

        n_groups = len(data)

        vals = [x[1] for x in data]
        legends = [x[0] for x in data]
        
        index = np.arange(n_groups)
        
        df_bar = pd.DataFrame({'word': legends, 'count':vals})
        
        plot = px.bar(data_frame = df_bar, 
                         x = 'word', 
                         y = 'count', 
                         title = 'Top 20 Words for Total Corpus of Chilean Twitter Users')
        plot.update_traces(marker_color = 'blue')
        
    return plot
    

# Run server
if __name__ == '__main__':
    app.run_server(debug = True)
