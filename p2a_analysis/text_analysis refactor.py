'''
Used to analyse p2a megamatrix with sentiment, frequency distribution, and wordcloud

This uses https://www.kirenz.com/post/2021-12-11-text-mining-and-sentiment-analysis-with-nltk-and-pandas-in-python/text-mining-and-sentiment-analysis-with-nltk-and-pandas-in-python/
as a basis 
'''

import pandas as pd
import numpy as np
import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk.stem import WordNetLemmatizer
from nltk.sentiment import SentimentIntensityAnalyzer
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('vader_lexicon')

# LA 1 = Sutton 
# LA 2 = Essex 
# LA 3 = Croydon 
# LA 4 = Camden

# Setting up dfs
df = pd.read_excel(r'/workspaces/D2I-Jupyter-Notebook-Tools/p2a_analysis/mega matrix - with analysis.xlsx',
                  'All data items')
df.columns = df.columns.str.lower()
sutton = df[['sutton text']].copy()
essex = df[['essex text']].copy()
croydon = df[['croydon text']].copy()
camden = df[['camden text']].copy()

sutton.dropna(inplace=True)
essex.dropna(inplace=True)
camden.dropna(inplace=True)
croydon.dropna(inplace=True)

sutton['text'] = sutton['sutton text'].astype(str).str.lower()
essex['text'] = essex['essex text'].astype(str).str.lower()
croydon['text'] = croydon['croydon text'].astype(str).str.lower()
camden['text'] = camden['camden text'].astype(str).str.lower()


total = pd.concat([sutton, camden, croydon, essex], axis=0).reset_index()

df_dict={'LA 1':sutton,
         'LA 2':essex,
         'LA 3':croydon,
         'LA 4':camden,
         'All LAs':total
         }
#print(df_dict['All LAs'])

regexp = RegexpTokenizer('\w+')
wordnet_lem = WordNetLemmatizer()
analyzer = SentimentIntensityAnalyzer()

stopwords = nltk.corpus.stopwords.words("english")
my_stopwords = ['child', 'young', 'person']
stopwords.extend(my_stopwords)


def make_wordcloud(df, la):
    
    df['token'] = df['text'].apply(regexp.tokenize)


    # Adding stopwords and removing from data
    df['token'] = df['token'].apply(lambda x: [item for item in x if item not in stopwords])

    # Keep only words longer than 2 letter
    df['string'] = df['token'].apply(lambda x: ' '.join([item for item in x if len(item)>2]))

    #  Lists of all words
    words = ' '.join([word for word in df['string']])

    # Tokenize all and frequency distribution
    tokenized = nltk.tokenize.word_tokenize(words)

    #Drop words appearing less than 3 times
    fdist = FreqDist(tokenized)
    df['string fdist'] = df['token'].apply(lambda x: ' '.join([item for item in x if fdist[item] >= 3 ]))

    # Lemmatization - grouping together similar words
    df['lem'] = df['string fdist'].apply(wordnet_lem.lemmatize)
    words_lem = ' '.join([word for word in df['lem']])


    #  Word cloud
    cloud = WordCloud(width=600,
                            height=400,
                            random_state=2,
                            max_font_size=100,
                            background_color='white',
                            colormap='tab20c',
                            repeat=True,
                            ).generate(words_lem)
    plt.title(f'{la} wordcloud')
    plt.figure(figsize=(10,7))
    plt.imshow(cloud, interpolation='bilinear')
    plt.axis('off');
    plt.savefig(f'p2a_analysis/{la} word cloud.png')
    plt.clf()

    #  Frequency distribution plot
    top_10 = fdist.most_common(10)
    fdist = pd.Series(dict(top_10))

    fig = px.bar(y=fdist.index, 
                 x=fdist.values,
                 title=f'{la} top 10 word distribution',
                 labels=dict(x="Word", y="Frequency"))

    # sort values
    fig.update_layout(barmode='stack', yaxis={'categoryorder':'total ascending'})

    # show plot
    fig.write_image(f"p2a_analysis/{la} fdist.png")

    
    # Sentiment analysis
    df['polarity'] = df['lem'].apply(lambda x: analyzer.polarity_scores(x))
    df = pd.concat(
        [df.drop(['polarity'], axis=1),
        df['polarity'].apply(pd.Series)], axis=1)
    
    df['sentiment'] = df['compound'].apply(lambda x: 'positive' if x>0 else 'neutral' if x==0 else 'negative')

    count_bar = sns.countplot(y='sentiment',
                data=df);
    plt.title(f'{la}: number of questions with positive, negative, and neutral sentiment')
    plt.xlabel('Sentiment')
    plt.ylabel('Number of questions')
    plt.savefig(f'p2a_analysis/{la} sentiment bar')
    plt.clf()

    count_box = sns.boxplot(y='compound',
                x='sentiment',
                data=df);
    plt.title(f'{la}: distribution of sentiment scores')
    plt.xlabel('Sentiment')
    plt.ylabel('Distribution of scores')
    plt.ylim(-1,1)
    plt.savefig(f'p2a_analysis/{la} sentiment box')

    return top_10, df

fdists = {}
combined_sentiment_dfs = {}
sent_df = pd.DataFrame({'Sentiment':['Neutral', 'Positive', 'Negative']})
for key, value in df_dict.items():
    plt.clf()
    fdist, sentiment_df = make_wordcloud(value, key)
    neutral_percent = (len(sentiment_df[sentiment_df['sentiment'] == 'neutral'])/len(sentiment_df))*100
    positive_percent = (len(sentiment_df[sentiment_df['sentiment'] == 'positive'])/len(sentiment_df))*100
    negative_percent = (len(sentiment_df[sentiment_df['sentiment'] == 'negative'])/len(sentiment_df))*100
    fdists[key] = fdist
    sent_df[key] = [neutral_percent, positive_percent, negative_percent]
    sentiment_df['LA'] = key
    combined_sentiment_dfs[key] = sentiment_df

plt.clf()
all_sentiments = pd.concat([combined_sentiment_dfs['LA 1'], 
                           combined_sentiment_dfs['LA 2'], 
                           combined_sentiment_dfs['LA 3'],
                           combined_sentiment_dfs['LA 4'], 
                           combined_sentiment_dfs['All LAs']], axis=0).reset_index()
all_sentiments = all_sentiments[['compound', 'LA', 'sentiment']]
no_neutral_sentiments = all_sentiments[all_sentiments['sentiment'] != 'neutral']
#all_sentiments = all_sentiments[all_sentiments['sentiment'] != 'neutral']

count_box = sns.boxplot(y='compound',
            x='sentiment',
            data=no_neutral_sentiments,
            hue='LA',);
plt.title(f'All LAs compared distribution of sentiment scores')
plt.xlabel('Sentiment')
plt.ylabel('Distribution of scores')
plt.ylim(-1,1)
plt.savefig(f'p2a_analysis/all LA sentiment box')

# positive/negative sentiment comparisons
plt.clf()
sent_df.plot(x="Sentiment", y=["LA 1", "LA 2", "LA 3", "LA 4", "All LAs"], kind="bar")
plt.title('Comparison of percentage of questions with positive and negative sentiments')
plt.ylabel('Percentage')
plt.xlabel('Sentiment')
plt.savefig(f'p2a_analysis/percentage sentiment comparison.png', bbox_inches='tight')


# Getting top ten words from each LA from tuples
sutton_10 = [i[0] for i in fdists['LA 1']]
essex_10 = [i[0] for i in fdists['LA 2']]
croydon_10 = [i[0] for i in fdists['LA 3']]
camden_10 = [i[0] for i in fdists['LA 4']]

top_10s_combined = sutton_10 + essex_10 + croydon_10 + camden_10 
#print(top_10s_combined)


la_word_count_dict = {}
def top_10_counts(df, la):
    # retain only rows containing words from the top 10 of every LA
    df['flag'] = np.where(df.text.str.contains('|'.join(top_10s_combined)),1,0)
    df = df[df['flag'] == 1]

    for word in top_10s_combined:
        word_df = df[df['text'].str.contains(word)]
        word_len = len(word_df)
        #print(f'{la}, {word}, {word_len}')
        la_word_count_dict[word] = word_len
    #print(la_word_count_dict)
    return la_word_count_dict

all_la_counts_dict = top_10_counts(df_dict['All LAs'], 'All LAs')
all_la_counts_df = pd.DataFrame(all_la_counts_dict.items(), columns=['word', f'{key} count'])


for key, value in df_dict.items():
    if key != 'All LAs':    
        temp_dict = top_10_counts(value, key)
        temp_df = pd.DataFrame(temp_dict.items(), columns=['word', f'{key} count'])
        all_la_counts_df = all_la_counts_df.merge(temp_df, on='word')



all_la_counts_df['LA 1 percentage'] = (all_la_counts_df['LA 1 count']/574)*100
all_la_counts_df['LA 2 percentage'] = (all_la_counts_df['LA 2 count']/434)*100
all_la_counts_df['LA 3 percentage'] = (all_la_counts_df['LA 3 count']/838)*100
all_la_counts_df['LA 4 percentage'] = (all_la_counts_df['LA 4 count']/473)*100
all_la_counts_df['All LA percentage'] = (all_la_counts_df['All LAs count']/2319)*100
#print(all_la_counts_df)
plt.clf()
all_la_counts_df.plot(x="word", y=["LA 1 percentage", "LA 2 percentage", "LA 3 percentage", "LA 4 percentage", "All LA percentage"], kind="bar")
plt.title('Percentage of questions from each LA using a word from the combined list of top 10 words from All LAs')
plt.ylabel('Percentage')
plt.xlabel('Word')

plt.savefig(f'p2a_analysis/percentage word counts.png', bbox_inches='tight')

# Finding questions all LAs collect that aren't 903 or Annex A
#print(df.info())
not_stat = df[(df['annex a  information captured'].isna()) &
               (df['903 information captured'].isna())]

not_stat_all_four = not_stat[(not_stat['sutton text'].notna()) &
                             (not_stat['essex text'].notna()) &
                             (not_stat['croydon text'].notna()) &
                             (not_stat['camden text'].notna())].reset_index()

#print(not_stat_all_four['sutton text'])
not_stat_all_four.to_csv('p2a_analysis/not_stat_all_four.csv', index=False)

# Length and percentage of Qs about feelings, views, &c.
feelings_words_short = ['view', 'feel', 'opinion']
feelings_words_long = ['view', 'feel', 'opinion', 'aspiration', 'emotional', 'well-being', 'wellbeing', 'identity'] 


# Data items unique to one LA
just_essex = df[(df['essex text'].notna()) &
                (df['sutton text'].isna()) &
                (df['croydon text'].isna()) &
                (df['camden text'].isna())]

just_sutton = df[(df['sutton text'].notna()) &
                (df['essex text'].isna()) &
                (df['croydon text'].isna()) &
                (df['camden text'].isna())]


just_croydon = df[(df['croydon text'].notna()) &
                (df['sutton text'].isna()) &
                (df['essex text'].isna()) &
                (df['camden text'].isna())]


just_camden = df[(df['camden text'].notna()) &
                (df['sutton text'].isna()) &
                (df['croydon text'].isna()) &
                (df['essex text'].isna())]
only_one_la_dict = {'LA 1':len(just_sutton),
                    'LA 2':len(just_essex),
                    'LA 3':len(just_croydon),
                    'LA 4':len(just_camden)}
just_one_df = pd.DataFrame(only_one_la_dict.items(), columns=['LA', 'Unique questions'])
plt.clf()
just_one_df.plot(x="LA", y='Unique questions', kind="bar", color=['blue', 'orange', 'green', 'red'])
plt.title('Questions unique to each LA')
plt.ylabel('Unique questions')
plt.xlabel('LA')
plt.legend('', frameon=False)
plt.savefig(f'p2a_analysis/unique questions.png', bbox_inches='tight')

for la, file in {'la 1':just_sutton, 'la 2':just_essex, 'la 3':just_croydon, 'la 4':just_camden}.items():
    file.to_csv(f'p2a_analysis/{la} unique qs.csv', index=False)

# Questions asked in only 3 LAs
no_la_1 = df[(df['sutton text'].isna()) & (df['essex text'].notna()) & (df['croydon text'].notna()) & (df['camden text'].notna())]
no_la_2 = df[(df['essex text'].isna()) & (df['sutton text'].notna()) & (df['croydon text'].notna()) & (df['camden text'].notna())]
no_la_3 = df[(df['croydon text'].isna()) & (df['essex text'].notna()) & (df['sutton text'].notna()) & (df['camden text'].notna())]
no_la_4 = df[(df['camden text'].isna()) & (df['essex text'].notna()) & (df['croydon text'].notna()) & (df['sutton text'].notna())]
only_3_dict = {'LA 1':len(no_la_1),
                'LA 2':len(no_la_2),
                'LA 3':len(no_la_3),
                'LA 4':len(no_la_4)}
only_3_df = pd.DataFrame(only_3_dict.items(), columns=['LA', 'Questions in three other LAs not in this LA'])
plt.clf()
only_3_df.plot(x="LA", y='Questions in three other LAs not in this LA', kind="bar", color=['blue', 'orange', 'green', 'red'])
plt.title('Number of questions in 3 LAs not in a given LA')
plt.ylabel('Number of questions not features')
plt.xlabel('LA')
plt.legend('', frameon=False)
plt.savefig(f'p2a_analysis/unique non questions.png', bbox_inches='tight')

for la, file in {'la 1':no_la_1, 'la 2':no_la_2, 'la 3':no_la_3, 'la 4':no_la_4}.items():
    file.to_csv(f'p2a_analysis/{la} no qs.csv', index=False)


# Voice of child plots
def feel_counts(df, list):
    df = df[(df['text'].str.contains('|'.join(list))) & (~df['text'].str.contains('review'))]
    #df = df[(df['text'].str.contains('|'.join(feelings_words_long)))]
    # print(df['text'])
    length = len(df)
    return length

feels_dict_short = {}
for key, value in df_dict.items():
    if key != 'All LAs':    
        length = feel_counts(value, feelings_words_short)
        feels_dict_short[key] = length

feels_dict_long = {}
for key, value in df_dict.items():
    if key != 'All LAs':    
        length = feel_counts(value, feelings_words_long)
        feels_dict_long[key] = length

feels_counts_df_short = pd.DataFrame(feels_dict_short.items(), columns=['LA', 'count'])
feels_counts_df_short.loc[feels_counts_df_short.LA == 'LA 1', 'Percentage'] = (feels_counts_df_short['count']/574)*100
feels_counts_df_short.loc[feels_counts_df_short.LA == 'LA 4', 'Percentage'] = (feels_counts_df_short['count']/473)*100
feels_counts_df_short.loc[feels_counts_df_short.LA == 'LA 2', 'Percentage'] = (feels_counts_df_short['count']/434)*100
feels_counts_df_short.loc[feels_counts_df_short.LA == 'LA 3', 'Percentage'] = (feels_counts_df_short['count']/838)*100

plt.clf()
feels_counts_df_short.plot(x="LA", y='Percentage', kind="bar", color=['blue', 'orange', 'green', 'red'])
plt.title('Percentage of questions using short list of words indicating a subjective view is observed')
plt.ylabel('Percentage')
plt.xlabel('LA')
plt.legend('', frameon=False)
plt.savefig(f'p2a_analysis/feels counts short.png', bbox_inches='tight')

feels_counts_df_long = pd.DataFrame(feels_dict_long.items(), columns=['LA', 'count'])
feels_counts_df_long.loc[feels_counts_df_long.LA == 'LA 1', 'Percentage'] = (feels_counts_df_long['count']/574)*100
feels_counts_df_long.loc[feels_counts_df_long.LA == 'LA 4', 'Percentage'] = (feels_counts_df_long['count']/473)*100
feels_counts_df_long.loc[feels_counts_df_long.LA == 'LA 2', 'Percentage'] = (feels_counts_df_long['count']/434)*100
feels_counts_df_long.loc[feels_counts_df_long.LA == 'LA 3', 'Percentage'] = (feels_counts_df_long['count']/838)*100

plt.clf()
feels_counts_df_long.plot(x="LA", y='Percentage', kind="bar", color=['blue', 'orange', 'green', 'red'])
plt.title(f'Percentage of questions using long list of words \n indicating a subjective view, or emotional state is observed')
plt.ylabel('Percentage')
plt.xlabel('LA')
plt.legend('', frameon=False)
plt.savefig(f'p2a_analysis/feels counts long.png', bbox_inches='tight')


# print(feels_counts_df_short)
# print(feels_counts_df_long)