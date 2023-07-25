'''
Used to analyse p2a megamatrix with sentiment, frequency distribution, and wordcloud

This uses https://www.kirenz.com/post/2021-12-11-text-mining-and-sentiment-analysis-with-nltk-and-pandas-in-python/text-mining-and-sentiment-analysis-with-nltk-and-pandas-in-python/
as a basis 
'''

import pandas as pd
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

df_dict={'sutton':sutton,
         'essex':essex,
         'croydon':croydon,
         'camden':camden,
         }

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
                            repeat=True,
                            ).generate(words_lem)
    plt.figure(figsize=(10,7))
    plt.imshow(cloud, interpolation='bilinear')
    plt.axis('off');
    plt.savefig(f'p2a_analysis/{la} word cloud.png')
    plt.clf()

    #  Frequency distribution plot
    top_10 = fdist.most_common(10)
    fdist = pd.Series(dict(top_10))
    
    fig = px.bar(y=fdist.index, x=fdist.values)

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
    plt.savefig(f'p2a_analysis/{la} sentiment bar')
    plt.clf()

    count_box = sns.boxplot(y='compound',
                x='sentiment',
                data=df);
    plt.savefig(f'p2a_analysis/{la} sentiment box')

for key, value in df_dict.items():
    plt.clf()
    make_wordcloud(value, key)
