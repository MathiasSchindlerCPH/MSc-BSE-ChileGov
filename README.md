<!---
<object data="https://drive.google.com/file/d/1k636xjMSPMQPJDPBj6cegNEgmXFL7tSu/preview" type="application/pdf" width="700px" height="700px">
    <embed src="https://drive.google.com/file/d/1k636xjMSPMQPJDPBj6cegNEgmXFL7tSu/preview">
        <p>This browser does not support PDFs. Please download the PDF to view it: <a href="https://drive.google.com/file/d/1k636xjMSPMQPJDPBj6cegNEgmXFL7tSu/preview">Download PDF</a>.</p>
    </embed>
</object>
--->

# Introduction
This is the git repository for the master thesis challenge from the Chilean Government by Andrés Couble, Mathias Schindler and  Kalliope Stassinos at the Data Science for Decision Making Program at the Barcelona School of Economics, Class of '22. The final document of the thesis is the file `Report_Thesis.pdf`.

# Challenge Task
The challenge task was stated by Claudio Villegas Oliva from the Chilean Communication Office as follows: 

*''Develop a methodology to analyze the Chilean conversation on Twitter on a specific topic, considering the political affiliation of the users. Describe the associated narratives that appear over time and the network structure of the groups involved. Apply the developed methodology using immigration as the test subject.''*


# Relevance
The Twittersphere is generally not representative of the whole population, so our social listening tool is not meant to replace traditional telephone- and survey-based opinion polls. It can however complement these methods at a higher frequency and at lower cost. Thereby it can help gauge concerns and agendas of this subset of the population and, in this way, be very useful for the Chilean Communication Office which is in charge of designing the government's communication strategy. 
        
Our developed social listening tool can raise alerts about unusual activity following unusual peaks in Twitter activity after specific events. Governments pay attention to many political topics simultaneously, so knowing that a certain topic has unusual Twitter activity is a helpful to know what issues need special attention. 
        
Tracking the metrics presented in this repository can give the Government insights into the content of tweets and thereby identify specific political agendas. Network analysis is useful to identify the most influential users, while distinguishing left- and right-leaning users is helpful to find which political affiliation is pushing which agendas within topics. Analyzing these metrics (e.g. using our interactive dashboard) can help the CCO better shape and target their rhetorical presentation of new policies. 
        
Our methodology takes approximately one day of computational execution time and can hence be updated on a daily basis for analyses. It requires some manual input in the initial execution, but for subsequent updates can run autonomously.


# Methodology
 We develop a methodology that, following 8 steps and with minimal manual input, allows the user to obtain most of the tweets about a given topic in a given country for a given period of time. The corpus from the methodology contains information about the political affiliation of the Twitter users, distinguishing them between left- and right-leaning. Finally, the methodology also allows practitioners to obtain the network of retweets between these users in the selected topic.
            
Considering that one of the scopes of our challenge is to provide a social listening tool that helps to monitor the conversation on time, we also provide scripts to subsequently update the data for new time periods. 
            
We analyze the corpus using a custom-tailored Python library considering simple textual measures such as word clouds, bigrams and hashtags. The interaction of Twitter users is analyzed using methods from networks analysis utilizing influence measures such as degree and centrality and interconnection measures such as density and reciprocity.


# Main Results
We find that our methodology works well in constructing a corpus with tweets about immigration, written by Chilean national Twitter users or authors in Chile. It also seems to work for feminism and can hence be utilized for many separate political topics. 
        
Regarding immigration in Chile from November 2020 to April 2022 we find that right-leaning Twitter users are more active, more influential and more interconnected than left-leaning users. Right-leaning users are mostly concerned with undocumented immigration and lately begin to relate immigration with crime. They also attempt to link immigration with terrorism. Left-leaning users are worried about these rising sentiments which they view as an expression of xenophobia and racism as seen from the figure below.

<p align="center">
  <img src="https://github.com/BSE-DSDM-2022/ChileGov/blob/master/figures/for_readme/fig_Proportion_of_Tweets_Containing_Specific_Subtopic_Related_Terms_by_Political_Affiliation_during_the_Protest.png" />
</p>

The current President is not particularly influential in the Chilean Twittersphere regarding immigration. The previous right-wing candidate José Kast was the most influential, as were some media outlets such as T13, Cooperativa and Biobio. This might be a challenge for the current government as they try to improve the current immigration situation. The table below shows the five most influential Twitter users. The figure shows the simplified entire network considered in this project.

<p align="center">
  <img src="https://github.com/BSE-DSDM-2022/ChileGov/blob/master/figures/for_readme/tab_Five_Most_Influential_Users_by_Degree_Centrality.png" />
</p>
<p align="center">
  <img src="https://github.com/BSE-DSDM-2022/ChileGov/blob/master/figures/for_readme/fig_Simplified_Undirected_General_Graph_of_Network.jpeg" />
</p>


# Recommendations and Limitationes
When the Government presents new immigration policies, they should emphasize their approach to the undocumented situation of migrants as well as crime when targeting a right-leaning audience. When targeting a left-leaning audience, they should emphasize that the policies are not a result of xenophobia. The Government should also prioritize to be visible on media outlets such as T13, Cooperativa and Biobio. In this way, the President might become more influential in the Chilean Twittersphere on immigration, as we have shown José Kast was substantially more influential in our studied time frame.
        
The Government should always keep in mind the potential bias in our sample when utilizing our developed social listening tool (despite our results being consistent with previous studies). They should always consider complementing findings with other studies such as opinion polls, focus groups, etc.


# Future Improvements
We suggest to prioritize improvement efforts on classification of political affiliation and bot detection. For more advanced results, including sentiment scores and topic modeling algorithms. Finally, the CCO can target efforts towards building a high-quality interactive dashboard as well as constructing more covariates such as gender or age.

# Usage of Social Listening Tool
Examples of our social listening tools use cases can be found in the folders `ChileGov/methodology_immigration` and `ChileGov/methodology_feminism` for usages about immigration in Chile and feminism in Chile, respectively. Our social listening tool requires acces to the Twitter API.

**Initial Runs**<br>
First-time executions of methodology should run scripts in the directory `ChileGov/methodology_blank/initial`. First-time executions require some manual input as clearly identified in each of the scripts. 

**Updating**<br>
Subsequent updates for new time periods should run scripts in `ChileGov/methodology_blank/update_existing/`. Such updates do not require manual input, except specifying the new time periods.

**Analyzing**<br>
For analyzing the corpora resulting form the methodology, users can use the social listening tools provided in `ChileGov/methodology_blank/z_explore_data/`. Here is the custom Python library `TxtAnLib` which is tailored to analyzing the corpora resulting from the methodology. Please refer to `ChileGov/methodology_blank/z_explore_data/README.md` for documentation on the `TxtAnLib` library.

**Data for Analyzed Topics**<br>
As mentioned, we already run the methodology for immigration between 1st November 2020 and 11th April 2022 (`ChileGov/methodology_immigration`) and for feminism between 9th March 2022 and 11th March 2022 and after we update it adding 12th March 2022 to 13th March 20222 (`ChileGov/methodology_feminism`). 
Considering that GitHub doesn't provide enough space to store all the files that methodologie produces, we deliver separately in a .zip-file with a clone of the whole repository, including the data. 
