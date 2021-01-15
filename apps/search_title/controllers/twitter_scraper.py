from twitterscraper import query_tweets
import datetime as dt
import numpy as np
import pandas as pd
import time
import re


def remove_quotation_mark(text):
    return text.replace("\"", "'")


def tweets_to_data_frame(tweets):
    df = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['tweets'])
    df['cleaned'] = np.array([remove_quotation_mark(clean(tweet.text)) for tweet in tweets])
    df['tweet_id'] = np.array([tweet.tweet_id for tweet in tweets])
    df['user_id'] = np.array([tweet.user_id for tweet in tweets])
    df['username'] = np.array([tweet.username for tweet in tweets])
    df['screen_name'] = np.array([tweet.screen_name for tweet in tweets])
    df['len'] = np.array([len(tweet.text) for tweet in tweets])
    df['date'] = np.array([tweet.timestamp for tweet in tweets])
    df['likes'] = np.array([tweet.likes for tweet in tweets])
    df['retweets'] = np.array([tweet.retweets for tweet in tweets])
    df['likes_and_retweets'] = np.array([tweet.retweets + tweet.likes for tweet in tweets])
    return df


def clean(tweet):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())


def get_tweets(hashtag):
    return query_tweets(query=hashtag, poolsize=4,
                        begindate=dt.date(2018, 12, 21),
                        enddate=dt.date(2018, 12, 22),
                        lang='en')


def remove_duplicates(df):
    return df.drop_duplicates(subset=None, keep='first', inplace=False)


def sort_tweets(df):
    for key, value in df.iterrows():
        pass
    return df.sort_values(by='date', ascending=False, inplace=False, kind='quicksort', na_position='last')


def create_and_start_new_job(hashtag):
    tweets_list = get_tweets(hashtag)
    tweets_df = tweets_to_data_frame(tweets_list)
    unique_tweets = remove_duplicates(tweets_df)
    sorted_tweets = sort_tweets(unique_tweets)
    return sorted_tweets


def get_highest_retweets(df, n):
    return df.nlargest(n, "likes_and_retweets")

# if __name__ == '__main__':
#     overall_time = time.time()
#     hashtag = "#Joker"
#     query_time = time.time()
#     list_of_tweets = query_tweets(query=hashtag, poolsize=4,
#                                   begindate=dt.date(2015, 1, 1),
#                                   enddate=dt.date(2015, 1, 2),
#                                   lang='en')
#     query_time = time.time() - query_time
#     print("number of tweets retrieved : " + str(len(list_of_tweets)))
#     print("query_time : " + str(query_time))
#     df = tweets_to_data_frame(list_of_tweets)
#     dropping_duplicates_time = time.time()
#     df.drop_duplicates(subset=None, keep='first', inplace=True)
#     dropping_duplicates_time = time.time() - dropping_duplicates_time
#     print("dropping_duplicates_time : " + str(dropping_duplicates_time))
#     sorting_time = time.time()
#     df.sort_values(by='date', ascending=False, inplace=True, kind='quicksort', na_position='last')
#     sorting_time = time.time() - sorting_time
#     print("sorting_time : " + str(sorting_time))
#     print("Top likes :")
#     __get_highest_likes(df, 10).to_html('./output/' + clean(hashtag) + 'toplikes 3.html')
#     print("Top retweets :")
#     __get_highest_retweets(df, 10).to_html('./output/' + clean(hashtag) + 'topretweets 3.html')
#     json_time = time.time()
#     df.to_json(path_or_buf='./output/' + clean(hashtag) + '4.json', date_format='iso')
#     json_time = time.time() - json_time
#     # print("json_time : " + str(json_time))
#     # html_time = time.time()
#     df.to_html('./output/' + clean(hashtag) + '3.html')
#     # html_time = time.time() - html_time
#     # print("html_time : " + str(html_time))
#     overall_time = time.time() - overall_time
#     print("overall_time : " + str(overall_time))
