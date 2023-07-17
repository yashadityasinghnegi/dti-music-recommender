# Music Recommender
This music reommendation system recommends users the similar songs based on the requested song, genre, current mood, and the era interested.
The system provide the chat interface implemented in Google Dialogflow for users to communicate by the nature languages.

### Envrionment Setup
1. **Data Preperation - Optional**. This step can be skipped as the source datasets are too large to be uploaded in the repo. The output dataset [df_comb_v5.csv](https://github.com/liaohaozhi/dti-music-recommender/blob/main/df_comb_v5.csv) is uploaded in the git.

2. **Mood Classification**. The notebook [mood_classification.ipynb](https://github.com/liaohaozhi/dti-music-recommender/blob/main/mood_classification.ipynb) reads the  [df_comb_v5.csv](https://github.com/liaohaozhi/dti-music-recommender/blob/main/df_comb_v5.csv) and trains a classificaiton model with the test data, and predicts each tuple's mood and output to the [df_comb_v5_with_mood.csv](https://github.com/liaohaozhi/dti-music-recommender/blob/main/df_comb_v5_with_mood.csv).

3. **Clustering**. The notebook [clustering.ipynb](https://github.com/liaohaozhi/dti-music-recommender/blob/main/clustering.ipynb) reads the [df_comb_v5_with_mood.csv](https://github.com/liaohaozhi/dti-music-recommender/blob/main/df_comb_v5_with_mood.csv) from the `Mood Classification`'s output dataset, and divides the songs to multiple clusters. The cluster numbers are evaluated by Elbow Method. The output dataset is [df_comb_v5_clustered.csv](https://github.com/liaohaozhi/dti-music-recommender/blob/main/df_comb_v5_clustered.csv).

4. **Start Flask Server Hosting Dialogflow Webhook**. The middletire server [app.py](https://github.com/liaohaozhi/dti-music-recommender/blob/main/app.py) host the `/webhooks` endpoint to process the Dialogflow requests, and returns the song recommendations. Workflow includes:
   1. Find the cluster of the requested song from the clustering dataset [df_comb_v5_clustered.csv](https://github.com/liaohaozhi/dti-music-recommender/blob/main/df_comb_v5_clustered.csv).
   2. Find the top 300 similiar songs for the requested song.
   3. Filter songs with genre, era and mood upon the request.
   4. Sort the recommendations based on their popularity.
   5. Return the top 5. 
To start the server, navigate to the root directory, run `flask run`.

5. **Host local Flask Server on Ngrok**. Install ngrok, and in terminal run `ngrok http http://127.0.0.1:5000`.

6. **Setup Dialogflow agent**. Import the agent with the backup zip. Go to Fulfillment and update the Webhook URL to the ngrok address ie. `https://f30b-74-15-253-93.ngrok.io/webhooks`.