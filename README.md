# Music Recommender
The music reommendation system recommends users the similar songs based on the requested song, genre, current mood, and the era interested.
The system provide the chat interface implemented in Google Dialogflow for users to communicate by the nature languages.

### Envrionment Setup
1. Data Preperation - Optional
This step can be skipped as the source datasets are too large to be uploaded in the repo. The output dataset `df_comb.csv` is uploaded in the git.

2. Mood Classification
The notebook [mood_classification.ipynb](https://github.com/liaohaozhi/dti-music-recommender/blob/main/mood_classification.ipynb) reads the `df_comb.csv` and trains a classificaiton model with the test data, and predicts each tuple in the `df_comb.csv` for its mood.

3. Clustering
The notebook [clustering.ipynb](https://github.com/liaohaozhi/dti-music-recommender/blob/main/clustering.ipynb) reads the output from the `Mood Classification` output dataset, and divides the songs to multiple clusters. The cluster numbers are evaluated by Elbow Method.

4. Start Flask Server Hosting Dialogflow Webhook
The middletire server host the `/webhooks` endpoint to process the Dialogflow requests, and returns the song recommendations. Workflow includes:
   1. Find the cluster of the requested song.
   2. Find the top 300 similiar songs for the requested song.
   3. Filter songs with genre, era and mood upon the request.
   4. Sort the recommendations based on their popularity.
   5. Return the top 5. 
To start the server, navigate to the root directory, run `flask run`.

5. Host local Flask Server on Ngrok.
Install ngrok, and in terminal run `ngrok http http://127.0.0.1:5000`.

6. Setup Dialogflow agent.
Import the agent with the backup zip. Go to Fulfillment and update the Webhook URL to the ngrok address ie. `https://f30b-74-15-253-93.ngrok.io/webhooks`.