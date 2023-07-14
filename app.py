from flask import Flask, request
import pandas
import nltk
import pandas as pd
import re
import random
import matplotlib.pyplot as plt
import numpy as np
from nltk.corpus import stopwords
#transform
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

nltk.download('stopwords')
nltk.download('wordnet')

def preprocess_text(text, stop_filter=True, flg_stemm=False, flg_lemm=True):
    ## clean (convert to lowercase and remove punctuations and characters and then strip)
    text = re.sub(r'[^\w\s]', '', str(text).lower().strip())
            
    ## Tokenize (convert from string to list)
    words = text.split()

    ## remove Stopwords
    if stop_filter:
        stop_word_set = set(stopwords.words("english"))
        words = [word for word in words if word not in stop_word_set]
                
    ## Stemming (remove -ing, -ly, ...)
    if flg_stemm == True:
        ps = nltk.stem.porter.PorterStemmer()
        words = [ps.stem(word) for word in words]
                
    ## Lemmatisation (convert the word into root word)
    if flg_lemm == True:
        lem = nltk.stem.wordnet.WordNetLemmatizer()
        words = [lem.lemmatize(word) for word in words]
            
    ## back to string from list
    text = " ".join(words)
    return text

def recommend_songs_based_on_lyric(song_name, count):
    idx = df[df['name']==song_name].index.tolist()[0]
    song_artist = df.iloc[idx].artists

    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    sim_scores = sim_scores[1:(count+1)]
    song_indcies = [i[0] for i in sim_scores]
    song_recos = []
    for song_index in song_indcies:
        print(df.at[song_index, 'name'])
        song_recos.append(df.at[song_index, 'name'])
    return song_recos


df = pd.read_csv('df_comb.csv')
df = df.sample(frac = 0.1, random_state=1).reset_index(drop=True)
df['clean lyric'] = df['Lyric'].apply(lambda x: preprocess_text(x))
cv = CountVectorizer()
tsm = cv.fit_transform(df['clean lyric'])
cosine_sim = cosine_similarity(tsm, tsm)

app = Flask(__name__)

@app.route("/webhooks", methods=['GET', 'POST'])
def webhooks():
    req = request.get_json(silent=True, force=True)
    print(req)
    queryResult = req['queryResult']
    action = queryResult['action']
    parameters = queryResult['parameters']
    return {
        "fulfillmentText": getResponseForAction(action, parameters)
    }

def getResponseForAction(action, parameters):
    if action == 'recommend-similar-songs':
        song_recos = recommend_songs_based_on_lyric(parameters['song'], 10)
        return 'Here are some songs you may like: ' + ','.join(song_recos)
    return 'Sorry, nothing found'