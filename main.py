from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax
import numpy as np 
import pandas as pd
from IPython.display import display
import json
from datetime import datetime
from tqdm import tqdm

import sqlite3
from pandas.io import sql


def sentiment(tweet):

    # preprocess tweet
    tweet_words = []

    for word in tweet.split(' '):
        if word.startswith('@') and len(word)>1:
            word = '@user'
        elif word.startswith('http'):
            word = 'http'
        tweet_words.append(word)

    tweet_proc = " ".join(tweet_words)

    # load model and tokenizer
    roberta = "cardiffnlp/twitter-roberta-base-sentiment"

    model = AutoModelForSequenceClassification.from_pretrained(roberta)
    tokenizer = AutoTokenizer.from_pretrained(roberta)

    labels = ['Negative', 'Neutral', 'Positive']

    # sentiment analysis
    encoded_tweet = tokenizer(tweet_proc, return_tensors='pt')

    output = model(**encoded_tweet)

    scores = output[0][0].detach().numpy()
    scores = softmax(scores)

    return scores

# Creating Dataframe from json lines
# pd.set_option('display.max_colwidth', None)
# lines = []
# with open(r'user-tweets.jsonl') as f:
#     lines = f.read().splitlines()
# line_dicts = [json.loads(line) for line in lines]
# df = pd.DataFrame(line_dicts)
# df.drop(['LinkToTweet','UserName','TweetEmbedCode'], axis=1, inplace=True)

# # Filtering dates after 01/06/2019
# df['CreatedAt'] = df['CreatedAt'].apply(lambda x: datetime.strptime(x[:-11],"%B %d, %Y"))
# date_filter = datetime.strptime('01/06/2019', '%d/%m/%Y')
# df = df.loc[df['CreatedAt']>=date_filter]

# # Cleaning up dataframe
# df['Text'] = df['Text'].astype('str')
# df = df[df['Text'].str.contains('Tesla')]
# # df = df.head(5)


# # Adding sentiment column
# df['sentiment'] = df['Text'].apply(lambda x: sentiment(x))
# df['positive'] = df['sentiment'].apply(lambda x: x[2])
# df['negative'] = df['sentiment'].apply(lambda x: x[0])
# df.drop(['sentiment'], axis=1, inplace=True)
# df = df[(df['positive']>=0.9) | (df['negative']>=0.9)]
# display(df)

# Writing to SQL Database
conn = sqlite3.connect("sen_twt.db")
cur = conn.cursor()
# df.to_sql("tweets", con=conn,if_exists = 'replace', index=False)

# pd.set_option('display.max_colwidth', None)

new = pd.read_sql_query("SELECT * from tweets", conn)
temp = pd.DataFrame(new, columns=["Text","CreatedAt","positive","negative"])
# arr = temp['CreatedAt'].tolist()
# arr = [x[:10] for x in arr]

display(temp)

# temp.to_sql("tweets", con=conn,if_exists = 'replace', index=False)

