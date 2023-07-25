'''
Used to analyse p2a megamatrix
'''

import pandas as pd
import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk.stem import WordNetLemmatizer
from wordcloud import WordCloud
import matplotlib.pyplot as plt

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')


df = pd.read_excel(r'/workspaces/D2I-Jupyter-Notebook-Tools/p2a_analysis/mega matrix - with analysis.xlsx',
                  'All data items')
df.columns = df.columns.str.lower()
questions_df = df[['croydon text', 'essex text', 'sutton text', 'camden text']]
df['croydon text'] = df['croydon text'].astype(str).str.lower()
df['essex text'] = df['essex text'].astype(str).str.lower()
df['sutton text'] = df['sutton text'].astype(str).str.lower()
df['camden text'] = df['camden text'].astype(str).str.lower()

#  Turning all words into regular expressions
regexp = RegexpTokenizer('\w+')
df['croydon token'] = df['croydon text'].apply(regexp.tokenize)
df['sutton token'] = df['sutton text'].apply(regexp.tokenize)
df['essex token'] = df['essex text'].apply(regexp.tokenize)
df['camden token'] = df['camden text'].apply(regexp.tokenize)

# Adding stopwords and removing from data
stopwords = nltk.corpus.stopwords.words("english")
my_stopwords = ['child', 'young', 'person']
stopwords.extend(my_stopwords)
df['camden token'] = df['camden token'].apply(lambda x: [item for item in x if item not in stopwords])
df['sutton token'] = df['sutton token'].apply(lambda x: [item for item in x if item not in stopwords])
df['essex token'] = df['essex token'].apply(lambda x: [item for item in x if item not in stopwords])
df['croydon token'] = df['croydon token'].apply(lambda x: [item for item in x if item not in stopwords])

# Keep only words longer than 2 letter
df['essex string'] = df['essex token'].apply(lambda x: ' '.join([item for item in x if len(item)>2]))
df['camden string'] = df['camden token'].apply(lambda x: ' '.join([item for item in x if len(item)>2]))
df['croydon string'] = df['croydon token'].apply(lambda x: ' '.join([item for item in x if len(item)>2]))
df['sutton string'] = df['sutton token'].apply(lambda x: ' '.join([item for item in x if len(item)>2]))

#  Lists of all words
sutton_words = ' '.join([word for word in df['sutton string']])
camden_words = ' '.join([word for word in df['camden string']])
essex_words = ' '.join([word for word in df['essex string']])
croydon_words = ' '.join([word for word in df['croydon string']])

# Tokenize all and frequency distribution
sutton_tokenized = nltk.tokenize.word_tokenize(sutton_words)
camden_tokenized = nltk.tokenize.word_tokenize(camden_words)
essex_tokenized = nltk.tokenize.word_tokenize(essex_words)
croydon_tokenized = nltk.tokenize.word_tokenize(croydon_words)
#Drop words appearing less than 3 times
sutton_fdist = FreqDist(sutton_tokenized)
essex_fdist = FreqDist(essex_tokenized)
camden_fdist = FreqDist(camden_tokenized)
croydon_fdist = FreqDist(croydon_tokenized)
df['sutton string fdist'] = df['sutton token'].apply(lambda x: ' '.join([item for item in x if sutton_fdist[item] >= 3 ]))
df['essex string fdist'] = df['essex token'].apply(lambda x: ' '.join([item for item in x if essex_fdist[item] >= 3 ]))
df['camden string fdist'] = df['camden token'].apply(lambda x: ' '.join([item for item in x if camden_fdist[item] >= 3 ]))
df['croydon string fdist'] = df['croydon token'].apply(lambda x: ' '.join([item for item in x if croydon_fdist[item] >= 3 ]))

# Lemmatization - grouping together similar words
wordnet_lem = WordNetLemmatizer()

df['sutton_lem'] = df['sutton string fdist'].apply(wordnet_lem.lemmatize)
df['essex lem'] = df['essex string fdist'].apply(wordnet_lem.lemmatize)
df['camden lem'] = df['camden string fdist'].apply(wordnet_lem.lemmatize)
df['croydon lem'] = df['croydon string fdist'].apply(wordnet_lem.lemmatize)

sutton_words_lem = ' '.join([word for word in df['sutton lem']])