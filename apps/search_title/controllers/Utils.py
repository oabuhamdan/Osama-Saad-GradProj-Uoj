import json
import re
import datetime as dt
from datetime import datetime
from ..models import Tweet


def get_json_from_file(file):
    data = open(file).read()
    response = json.loads(data.replace("'", "\""))
    return response


def log_info(data):
    log_data(data, 'info')


def log_error(data):
    log_data(data, 'error')


def log_data(data, type):
    header = ''
    log_file = open("log.txt", "a")
    time_stamp = datetime.now().strftime("%d-%m-%Y@%H:%M:%S")

    if type == 'info':
        header = 'INFO'
    elif type == 'error':
        header = 'ERROR'

    log_file.write(str(time_stamp))
    log_file.write(' | ')
    log_file.write(header)
    log_file.write(' | ')
    log_file.write(str(data))
    log_file.write("\n")
    log_file.close()


def clean(tweet):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())


def convert_to_hashtag(string):
    return "#" + ''.join(x for x in clean(string.title()) if not x.isspace())


# date form is day month year 2 chars for day 3 chars for month 4 chars for year 01 234 5678
def get_date(date):
    day = int(date[0:2])
    month = month_to_int(date[3:6])
    year = int(date[7:11])
    return dt.date(year, month, day)


def get_next_date(date):
    day = int(date[0:2])
    month = month_to_int(date[3:6])
    year = int(date[7:11])
    if month == 12:
        month = 1
        year += 1
    else:
        month += 1
    return dt.date(year, month, day)


def get_URL(title, year):
    return 'result/?search_title={}&year={}'.format(title.replace(' ', '+'), year)


def month_to_int(month):
    switcher = {
        "Jan": 1,
        "Feb": 2,
        "Mar": 3,
        "Apr": 4,
        "May": 5,
        "Jun": 6,
        "Jul": 7,
        "Aug": 8,
        "Sep": 9,
        "Oct": 10,
        "Nov": 11,
        "Dec": 12,
    }
    return switcher.get(month)


def parse_tweets(tweets):
    tokens = []
    top_tweets = []
    token = ''
    for char in tweets:
        if char == '|':
            tokens.append(token)
            token = ''
        elif char == '&':
            tokens.append(token)
            top_tweets.append(
                Tweet(tokens[0], tokens[1], tokens[2], tokens[3], tokens[4], tokens[5], tokens[6], tokens[7], tokens[8],
                      tokens[9]
                      ))
            token = ''
            tokens = []
        else:
            token += char
    return top_tweets


def parse_tweets_json(json_str):
    data = json.loads(json_str)
    top_tweets = []
    for tweet in data['tweets']:
        top_tweets.append(
            Tweet(tweet['text'], tweet['tweet_id'], tweet['user_id'], tweet['username'], tweet['screen_name'],
                  tweet['len'], tweet['date'], tweet['likes'], tweet['retweets'], tweet['likes_and_retweets'],
                  ))
    return top_tweets


def get_top_tweets_json(tweets):
    top_tweets = []

    for key, value in tweets.iterrows():
        top_tweets.append(
            Tweet(str(value['tweets']), str(value['tweet_id']), str(value['user_id']), str(value['username']),
                  str(value['screen_name']), str(value['len']), str(value['date']), str(value['likes']),
                  str(value['retweets']),
                  str(value['likes_and_retweets'])))
    top_tweets_json = '''{{"tweets":{0}}}'''.format(json.dumps([tweet.__dict__ for tweet in top_tweets]))
    return top_tweets, top_tweets_json
