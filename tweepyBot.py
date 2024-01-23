import tweepy
from tweepy import OAuthHandler

import json, http.client

from datetime import datetime
from itertools import count
import time
import re

import MetaTrader5 as mt5

# Twitter dev account credentials
consumer_key = "consumer_key"
consumer_secret = "consumer_secret"
access_key = "access_key"
access_secret = "access_secret"

#text sentiment API key
sentiment_key = "sentiment_key"

# Pass twitter credentials to tweepy via its OAuthHandler
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

# connect to the trade account without specifying a password and a server
mt5.initialize()

# account number in the top left corner of the MT5 terminal window
# the terminal database password is applied if connection data is set to be remembered
account_number = 5022145401
password = ''
authorized = mt5.login(account_number)

if authorized:
    print(f'Connected to the account')
else:
    print(f'failed to connect, error code: {mt5.last_error()}')