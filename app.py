from flask import Flask, request
import pandas as pd
import numpy as np
#transform
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def recommend_songs_based_on_lyric(filtered_df, similarities, song_name, count):
    idx = filtered_df[filtered_df['name']==song_name].index.tolist()[0]

    sim_scores = list(enumerate(similarities[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    sim_scores = sim_scores[1:(count+1)]
    song_indcies = [i[0] for i in sim_scores]
    song_recos = []
    for song_index in song_indcies:
        print(filtered_df.at[song_index, 'name'])
        song_recos.append(filtered_df.at[song_index, 'name'])
    return song_recos

def filter_df_for_song(song_name, genre, mood):
    row_record = df[df['name']==song_name].to_dict('records')[0]
    cluster_df = df[df['cluster'] == row_record['cluster']].reset_index(drop=True)
    filtered_df = cluster_df
    if genre:
        mask = filtered_df['Genres'].apply(lambda x: genre in x)
        filtered_df = filtered_df[mask]
    if mood:
        filtered_df = filtered_df[filtered_df['mood']==mood]
    #Incase filtered df dones't contains the row any more, add it back
    if (filtered_df['name']==song_name).any() == False:
        filtered_df = pd.concat([filtered_df, pd.DataFrame([row_record])], ignore_index=True)
    return filtered_df.reset_index(drop=True)

def calcualte_similarities(filtered_df):
    cv = CountVectorizer()
    tsm = cv.fit_transform(filtered_df['clean lyric'])
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
        genre = None
        mood = None
        if genre in parameters:
            genre = parameters['genre']
        if mood in parameters:
            mood = parameters['mood']
        filtered_df = filter_df_for_song(song_name, genre, mood)
        similiarities = calcualte_similarities(filtered_df)
        song_recos = recommend_songs_based_on_lyric(filtered_df, similiarities, song_name, 10)
        if len(song_recos) == 0:
            return f'I can not find any song like ${song_name}. Can you try another song?'
        return 'Here are some songs you may like: ' + ', '.join(song_recos)
    return 'Sorry, I can not understand you. Can you say again?'