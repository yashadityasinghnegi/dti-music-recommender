from flask import Flask, request
import pandas as pd
import numpy as np
#transform
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def recommend_songs_based_on_lyric(cluster_df, similarities, song_name, count):
    idx = cluster_df[cluster_df['name']==song_name].index.tolist()[0]

    sim_scores = list(enumerate(similarities[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    sim_scores = sim_scores[1:(count+1)]
    song_indcies = [i[0] for i in sim_scores]
    song_recos = []
    for song_index in song_indcies:
        print(cluster_df.at[song_index, 'name'])
        song_recos.append(cluster_df.at[song_index, 'name'])
    return song_recos

def find_cluster_for_song(song_name):
    idx = df[df['name']==song_name].index.tolist()[0]
    cluster_df = df[df['cluster'] == df.iloc[idx].cluster].reset_index(drop=True)
    return cluster_df

def calcualte_similarities(cluster_df):
    cv = CountVectorizer()
    tsm = cv.fit_transform(cluster_df['clean lyric'])
    cosine_sim = cosine_similarity(tsm, tsm)
    return cosine_sim

df = pd.read_csv('df_clustered.csv')
app = Flask(__name__)

@app.route("/webhooks", methods=['GET', 'POST'])
def webhooks():
    req = request.get_json(silent=True, force=True)
    print(req)
    queryResult = req['queryResult']
    action = queryResult['action']
    parameters = queryResult['parameters']
    return {
        "fulfillmentText": get_response_for_action(action, parameters)
    }

def get_response_for_action(action, parameters):
    if action == 'recommend-similar-songs':
        song_name = parameters['song']
        cluster_df = find_cluster_for_song(song_name)
        similiarities = calcualte_similarities(cluster_df)
        song_recos = recommend_songs_based_on_lyric(cluster_df, similiarities, parameters['song'], 10)
        return 'Here are some songs you may like: ' + ','.join(song_recos)
    return 'Sorry, nothing found'