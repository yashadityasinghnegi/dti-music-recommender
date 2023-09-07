# Music Recommender
This music recommendation system recommends users the similar songs based on the requested song, genre, current mood, and the era interested.
The system provide the chat interface implemented in Google Dialogflow for users to communicate by the nature languages.

### Envrionment Setup
0. **Data set sources**. Dataset with lyrics and genre tags: [Genres and Lyrics](https://www.kaggle.com/datasets/neisse/scrapped-lyrics-from-6-genres?select=artists-data.csv). Dataset with audio features: [Music features](https://www.kaggle.com/datasets/yamaerenay/spotify-dataset-19212020-600k-tracks?select=tracks.csv)

1. **Data Preperation - Optional**. This step can be skipped as the source datasets are too large to be uploaded in the repo. The output dataset [df_comb.csv](https://github.com/liaohaozhi/dti-music-recommender/blob/main/df_comb.csv) is uploaded in the git.

2. **Mood Classification**. The notebook [mood_classification.ipynb](https://github.com/liaohaozhi/dti-music-recommender/blob/main/mood_classification.ipynb) reads the [df_comb.csv](https://github.com/liaohaozhi/dti-music-recommender/blob/main/df_comb.csv) and trains a classificaiton model with the test data, and predicts each tuple's mood and output to the [df_comb_with_mood.csv](https://github.com/liaohaozhi/dti-music-recommender/blob/main/df_comb_with_mood.csv).

3. **Clustering**. The notebook [clustering.ipynb](https://github.com/liaohaozhi/dti-music-recommender/blob/main/clustering.ipynb) reads the [df_comb_with_mood.csv](https://github.com/liaohaozhi/dti-music-recommender/blob/main/df_comb_with_mood.csv) from the `Mood Classification`'s output dataset, and divides the songs to multiple clusters. The cluster numbers are evaluated by Elbow Method. The output dataset is [df_comb_clustered.csv](https://github.com/liaohaozhi/dti-music-recommender/blob/main/df_comb_clustered.csv).

4. **Start Flask Server Hosting Dialogflow Webhook**. The middletire server [app.py](https://github.com/liaohaozhi/dti-music-recommender/blob/main/app.py) host the `/webhooks` endpoint to process the Dialogflow requests, and returns the song recommendations. Workflow includes:
   1. Find the cluster of the requested song from the clustering dataset [df_comb_clustered.csv](https://github.com/liaohaozhi/dti-music-recommender/blob/main/df_comb_clustered.csv).
   2. Find the top 300 similiar songs for the requested song.
   3. Filter songs with genre, era and mood upon the request.
   4. Sort the recommendations based on their popularity.
   5. Return the top 5. 
To start the server, navigate to the root directory, run `flask run`.

5. **Host local Flask Server on Ngrok**. Install ngrok, and in terminal run `ngrok http http://127.0.0.1:5000`.

6. **Setup Dialogflow agent**. Import the agent with the backup zip. Go to Fulfillment and update the Webhook URL to the ngrok address ie. `https://f30b-74-15-253-93.ngrok.io/webhooks`.

7. **Classification comparison**. The classification algorithms and their results/accuracies can be compared by running [classification_comparison.ipynb](https://github.com/liaohaozhi/dti-music-recommender/blob/main/classification_compare.ipynb) after the above steps (separate from dialogFlow fulfillment) 
