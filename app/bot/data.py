from io import StringIO
#from pandas_schema import Column, Schema
#from pandas_schema.validation import LeadingWhitespaceValidation, TrailingWhitespaceValidation, CanConvertValidation, MatchesPatternValidation, InRangeValidation, InListValidation
import pandas as pd
import nltk
import re
import json
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

tweetFile = "tcs_tweets.csv"

def removeForCount(row):
    str1 = re.sub("http[\S]*( |$)","",row)
    str1 = re.sub("&amp;( |^)","",str1)
    str1 = re.sub("[\(\)\.,\":@&;%?\-'’/!]","", str1)
    str1 = re.sub("(^| )[a-zA-Z]{,2}(?= )","",str1)
    str1 = re.sub("(^| )[a-zA-Z]*[0-9][a-zA-Z0-9]*","", str1)
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(str1)
    filtered_sentence = [w for w in words if w not in stop_words]
    final = ' '.join(filtered_sentence)
    final = re.sub("# ","#", final)
    return final

#filtered_sentence = []

#for w in word_tokens:
#    if w not in stop_words:
#        filtered_sentence.append(w)

#print(word_tokens)
#print(filtered_sentence)

#spark = SparkSession.builder.master("local").appName("Word Count") .config("spark.some.config.option", "some-value").getOrCreate()
schema = "search_type string ,username string,retweet_count int,created_at datetime ,favourite_count int ,hashtags string,tweet_id long,text string,location string ,to string ,mined_at datetime ,quote_username string"

#schema = "date date ,serial_number string ,model string ,capacity_bytes long ,failure float ,smart_5_raw float ,smart_9_raw float ,smart_187_raw float ,smart_188_raw float ,smart_193_raw float ,smart_194_raw float ,smart_197_raw float ,smart_198_raw float ,smart_241_raw float ,smart_242_raw float "
#df = pd.read.option("header",True ).schema(schema).csv(logFile)
df = pd.read_csv(tweetFile, skiprows = 1, names=['search_type','username','retweet_count','created_at','favourite_count','hashtags','tweet_id','text','location','to','mined_at','quote_username'])
#print(df.head(5))
df["created_at"] = pd.to_datetime(df["created_at"])
#df["mined_at"] = pd.to_datetime(df["mined_at"])
df_this = df
df_this= df_this.replace()
#print(df_this["text"].isnan)
df_this["final"] = df_this["text"].apply(removeForCount)
#df_this.apply()
#print(df_this["created_at"].count())

#print(df["username"].unique())
use_user="tcs"
#df_this = df_this[df_this['username'].str.contains("(?i)"+use_user+"$")]
#print(df_this["final"].isnan)
print("**"*100)
data = df_this["final"].str.split(expand=True).stack().value_counts().head(25).to_dict()

data = json.dumps(data)

print(data)
#import calendar

#print ({v: k for k,v in enumerate(calendar.month_abbr)})

#removeForCount("this is a line with a long sentence")