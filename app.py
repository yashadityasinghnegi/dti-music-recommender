from flask import Flask, request
import pandas as pd
import numpy as np
#transform
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def recommend_songs_based_on_lyric(song_name, count):
    row_record = df[df['name']==song_name].to_dict('records')[0]
    cluster_df = df[df['cluster'] == row_record['cluster']].reset_index(drop=True)
    similiarities = calcualte_similarities(cluster_df)
    idx = cluster_df[cluster_df['name']==song_name].index.tolist()[0]
    sim_scores = list(enumerate(similiarities[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:(count+1)]
    song_indcies = [i[0] for i in sim_scores]
    return cluster_df.iloc[song_indcies].reset_index(drop=True)

def filter_df_for_song(reco_df, song_name, genre, mood, decade):
    # row_record = df[df['name']==song_name].to_dict('records')[0]
    filtered_df = reco_df
    print("top of filter - Recommendation based on genre:  " + str(genre))
    print("top of filter - Recommendation based on mood:   " + str(mood))
    print("top of filter - Recommendation based on decade: " + str(decade))
    if genre:
        mask = filtered_df['Genres'].apply(lambda x: genre in x)
        filtered_df = filtered_df[mask]
    if mood:
        filtered_df = filtered_df[filtered_df['mood']==mood]
    if decade:
        if decade == '1930s':
                filtered_df = filtered_df.loc[(df['release_date'] >= '1930-01-01') & (df['release_date'] < '1940-01-01')]
        elif decade == '1940s':
                filtered_df = filtered_df.loc[(df['release_date'] >= '1940-01-01') & (df['release_date'] < '1950-01-01')]
        elif decade == '1950s':
                filtered_df = filtered_df.loc[(df['release_date'] >= '1950-01-01') & (df['release_date'] < '1960-01-01')]
        elif decade == '1960s':
                filtered_df = filtered_df.loc[(df['release_date'] >= '1960-01-01') & (df['release_date'] < '1970-01-01')]
        elif decade == '1970s':
                filtered_df = filtered_df.loc[(df['release_date'] >= '1970-01-01') & (df['release_date'] < '1980-01-01')]
        elif decade == '1980s':
                filtered_df = filtered_df.loc[(df['release_date'] >= '1980-01-01') & (df['release_date'] < '1990-01-01')]
        elif decade == '1990s':
                filtered_df = filtered_df.loc[(df['release_date'] >= '1990-01-01') & (df['release_date'] < '2000-01-01')]
        elif decade == '2000s':
                filtered_df = filtered_df.loc[(df['release_date'] >= '2000-01-01') & (df['release_date'] < '2010-01-01')]
        elif decade == '2010s':
                filtered_df = filtered_df.loc[(df['release_date'] >= '2010-01-01') & (df['release_date'] < '2020-01-01')]
        elif decade == '2020s':
                filtered_df = filtered_df.loc[(df['release_date'] >= '2020-01-01')]

    #Incase filtered df dones't contains the row any more, add it back
    # if (filtered_df['name']==song_name).any() == False:
        # filtered_df = pd.concat([filtered_df, pd.DataFrame([row_record])], ignore_index=True)
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
    # if action == 'recommend-similar-songs':
    song_name = parameters['song']
    genre = None
    mood = None
    decade = None
    print("parameters: " + str(parameters))
    if parameters['genre']:
        genre = parameters['genre']
    if parameters['mood']:
        mood = parameters['mood']
    if parameters['decade']:
        decade = parameters['decade']
    #find top 300 recos in the cluster
    reco_df = recommend_songs_based_on_lyric(song_name, 300)
    print("Recommendation size: " + str(reco_df.shape[0]))
    #filter based on the requested attributes
    filtered_df = filter_df_for_song(reco_df, song_name, genre, mood, decade)
    print("Filtered Recommendation size: " + str(filtered_df.shape[0]))
    #sort by popurialtiy and return top 5
    filtered_df = filtered_df.sort_values(by=['popularity'], ascending=False)
    #return top 5 songs
    song_recos = []
    reco_number = 5
    for index, row in filtered_df.head(reco_number).iterrows():
        print(row['name'])
        song_recos.append(row['name'])
    if len(song_recos) == 0:
        return f'I can not find any song like {song_name}. Can you try another song?'
    return 'Here are some songs you may like: ' + ', '.join(song_recos)