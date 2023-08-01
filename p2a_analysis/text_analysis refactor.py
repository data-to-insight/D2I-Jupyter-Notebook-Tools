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

df_dict={'Sutton':sutton,
         'Essex':essex,
         'Croydon':croydon,
         'Camden':camden,
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

    return top_10

fdists = {}
for key, value in df_dict.items():
    plt.clf()
    fdist = make_wordcloud(value, key)
    fdists[key] = fdist


# Getting top ten words from each LA from tuples
sutton_10 = [i[0] for i in fdists['Sutton']]
essex_10 = [i[0] for i in fdists['Essex']]
croydon_10 = [i[0] for i in fdists['Croydon']]
camden_10 = [i[0] for i in fdists['Camden']]

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



all_la_counts_df['sutton percentage'] = (all_la_counts_df['Sutton count']/574)*100
all_la_counts_df['camden percentage'] = (all_la_counts_df['Camden count']/473)*100
all_la_counts_df['essex percentage'] = (all_la_counts_df['Essex count']/434)*100
all_la_counts_df['croydon percentage'] = (all_la_counts_df['Croydon count']/838)*100
all_la_counts_df['All LA percentage'] = (all_la_counts_df['All LAs count']/2319)*100
#print(all_la_counts_df)
plt.clf()
all_la_counts_df.plot(x="word", y=["sutton percentage", "essex percentage", "camden percentage", "croydon percentage", "All LA percentage"], kind="bar")
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
feels_counts_df_short.loc[feels_counts_df_short.LA == 'Sutton', 'Percentage'] = (feels_counts_df_short['count']/574)*100
feels_counts_df_short.loc[feels_counts_df_short.LA == 'Camden', 'Percentage'] = (feels_counts_df_short['count']/473)*100
feels_counts_df_short.loc[feels_counts_df_short.LA == 'Essex', 'Percentage'] = (feels_counts_df_short['count']/434)*100
feels_counts_df_short.loc[feels_counts_df_short.LA == 'Croydon', 'Percentage'] = (feels_counts_df_short['count']/838)*100

plt.clf()
feels_counts_df_short.plot(x="LA", y='Percentage', kind="bar")
plt.title('Percentage of questions using short list of words indicating a subjective view is observed')
plt.ylabel('Percentage')
plt.xlabel('LA')

plt.savefig(f'p2a_analysis/feels counts short.png', bbox_inches='tight')

feels_counts_df_long = pd.DataFrame(feels_dict_long.items(), columns=['LA', 'count'])
feels_counts_df_long.loc[feels_counts_df_long.LA == 'Sutton', 'Percentage'] = (feels_counts_df_long['count']/574)*100
feels_counts_df_long.loc[feels_counts_df_long.LA == 'Camden', 'Percentage'] = (feels_counts_df_long['count']/473)*100
feels_counts_df_long.loc[feels_counts_df_long.LA == 'Essex', 'Percentage'] = (feels_counts_df_long['count']/434)*100
feels_counts_df_long.loc[feels_counts_df_long.LA == 'Croydon', 'Percentage'] = (feels_counts_df_long['count']/838)*100

plt.clf()
feels_counts_df_long.plot(x="LA", y='Percentage', kind="bar")
plt.title('Percentage of questions using long list of words indicating a subjective view, or emotional state is observed')
plt.ylabel('Percentage')
plt.xlabel('LA')

plt.savefig(f'p2a_analysis/feels counts long.png', bbox_inches='tight')


print(feels_counts_df_short)
print(feels_counts_df_long)