# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import  AllSlotsReset
from rasa_sdk.executor import CollectingDispatcher
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

import pandas as pd
import re
import time
import json
#
#
tweetFile = "tcs_tweets.csv"
df = pd.read_csv(tweetFile,skiprows=1, names=['search_type','username','retweet_count','created_at','favourite_count','hashtags','tweet_id','text','location','to','mined_at','quote_username'])
df["created_at"] = pd.to_datetime(df["created_at"])
df["mined_at"] = pd.to_datetime(df["mined_at"])
df["retweet_count"] = pd.to_numeric(df["retweet_count"])
df["favourite_count"] = pd.to_numeric(df["favourite_count"])
df["tweet_id"] = pd.to_numeric(df["tweet_id"])

def removeForCount(row):
    str1 = re.sub("http[\S]*( |$)","",row)
    str1 = re.sub("&amp;( |^)","",str1)
    str1 = re.sub("[()\.,\":@&;%?\-'’/!]","", str1)
    str1 = re.sub("(^| )[a-zA-Z]{,2}(?= )","",str1)
    str1 = re.sub("(^| )[a-zA-Z]*[0-9][a-zA-Z0-9]*","", str1)
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(str1)
    filtered_sentence = [w for w in words if w not in stop_words]
    final = ' '.join(filtered_sentence)
    final = re.sub("# ","#", final)
    return final

def monthToNumber (month):
    if len(month) == 3:
        return time.strptime(month, "%b").tm_mon

    return time.strptime(month, "%B").tm_mon

class tweets_word_freq(Action):
    def name(self) -> Text:
        return "action_tweets_by_keyword"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text,Any]]:

        time=tracker.get_slot('time')
        username=tracker.get_slot('username')

        df_this = df
        df_this = df_this.replace()

        # df_this.dropna(
        #     axis=0,
        #     how='any',
        #     thresh=None,
        #     subset=df_this["text"],
        #     inplace=True
        # )
        df_this["final"] = df_this["text"].apply(removeForCount)

        # if time is not None:
        #     df_this = df_this[df_this["created_at"].dt.month == monthToNumber(time)]
        #
        if username is not None:
            if username[0] == '@':
                use_user = username[1:]
            else:
                use_user = username
            df_this = df_this[df_this['username'].str.contains("(?i)"+use_user+"$")]

        data = df_this["final"].str.split(expand=True).stack().value_counts().head(25).to_dict()

        data = json.dumps(data)

        #print(data)

        #print("Time in action is "+time)
        dispatcher.utter_message(data)
        return [AllSlotsReset()]

class tweets_count_by_time(Action):
    def name(self) -> Text:
        return "action_tweets_count_by_time"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text,Any]]:

        time=tracker.get_slot('time')
        username=tracker.get_slot('username')

        if time is None:
            dispatcher.utter_message(text="For which month would you like to know?")
            return []

        df_this = df[df["created_at"].dt.month == monthToNumber(time)]

        text = '''There were {} tweets in {} '''.format(  df_this["created_at"].count() , time )

        if username is not None:
            if username[0] == '@':
                use_user = username[1:]
            else:
                use_user = username

            df_this = df_this[df_this['username'].str.contains("(?i)"+use_user+"$")]
            text = '''{} made {} tweets in {} '''.format( username, df_this["created_at"].count(), time )


        #print("Time in action is "+time)
        dispatcher.utter_message(text=text)
        return [AllSlotsReset()]



class top_hashtag(Action):
    def name(self) -> Text:
        return "action_hashtag_count"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text,Any]]:

        time=tracker.get_slot('time')
        username=tracker.get_slot('username')

        df_this = df

        if time is not None:
            df_this = df_this[df_this["created_at"].dt.month == monthToNumber(time)]

        if username is not None:
            if username[0] == '@':
                use_user = username[1:]
            else:
                use_user = username

            df_this = df_this[df_this['username'].str.contains("(?i)"+use_user+"$")]

        data = df_this[df_this["Firm_Name"].str.split(expand=True).stack().value_counts()]


        #print("Time in action is "+time)
        dispatcher.utter_message(text=data)
        return [AllSlotsReset()]

class hashtag_trend(Action):
    def name(self) -> Text:
        return "action_hashtag_trend"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text,Any]]:

        time=tracker.get_slot('time')
        username=tracker.get_slot('username')

        df_this = df

        if time is not None:
            df_this = df_this[df_this["created_at"].dt.month == monthToNumber(time)]

        if username is not None:
            if username[0] == '@':
                use_user = username[1:]
            else:
                use_user = username

            df_this = df_this[df_this['username'].str.contains("(?i)"+use_user+"$")]

        data = df_this[df_this["Firm_Name"].str.split(expand=True).stack().value_counts()]


        #print("Time in action is "+time)
        dispatcher.utter_message(text=data)
        return [AllSlotsReset()]

class top_retweeted(Action):
    def name(self) -> Text:
        return "action_top_retweeted_tweet"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text,Any]]:

        time=tracker.get_slot('time')
        username=tracker.get_slot('username')

        df_this = df

        if time is not None:
            df_this = df_this[df_this["created_at"].dt.month == monthToNumber(time)]

        if username is not None:
            if username[0] == '@':
                use_user = username[1:]
            else:
                use_user = username

            df_this = df_this[df_this['username'].str.contains("(?i)"+use_user+"$")]

        data = df_this[df_this["Firm_Name"].str.split(expand=True).stack().value_counts()]


        #print("Time in action is "+time)
        dispatcher.utter_message(text=data)
        return [AllSlotsReset()]

class top_liked(Action):
    def name(self) -> Text:
        return "action_most_liked_tweet"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text,Any]]:

        time=tracker.get_slot('time')
        username=tracker.get_slot('username')

        df_this = df

        if time is not None:
            df_this = df_this[df_this["created_at"].dt.month == monthToNumber(time)]

        if username is not None:
            if username[0] == '@':
                use_user = username[1:]
            else:
                use_user = username

            df_this = df_this[df_this['username'].str.contains("(?i)"+use_user+"$")]

        data = df_this[df_this["Firm_Name"].str.split(expand=True).stack().value_counts()]


        #print("Time in action is "+time)
        dispatcher.utter_message(text=data)
        return [AllSlotsReset()]