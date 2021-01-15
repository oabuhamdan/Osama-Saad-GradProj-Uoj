import time

import numpy as np
import pandas as pd
from twitterscraper import query_tweets
import psycopg2
from ..models import TopTweet
from .S3Helper import upload_file_to_s3
from .Utils import log_info, clean, get_top_tweets_json


class ScrappingJob:
    __hashtag = ''
    __job_name = ''
    __from_date = ''
    __to_date = ''
    __lang = ''

    def __init__(self, hashtag, job_name, from_date, to_date, lang):
        self.__hashtag = hashtag
        self.__job_name = job_name
        self.__from_date = from_date
        self.__to_date = to_date
        self.__lang = lang

    def create_and_start_new_job(self):
        tweets_list = self.__get_tweets()
        tweets_df = self.__tweets_to_data_frame(tweets_list)
        unique_tweets = self.__remove_duplicates(tweets_df)
        sorted_tweets = self.__sort_tweets(unique_tweets)
        cleaned_tweets = self.__clean_tweets(sorted_tweets['tweets'])
        self.__write_and_upload_processed_tweets(cleaned_tweets)
        top_tweets = self.get_highest_likes_and_retweets(sorted_tweets, 10)
        top_tweets, top_tweets_json = get_top_tweets_json(top_tweets)
        tweets = TopTweet.create(top_tweets_json, self.__job_name)
        tweets.save()

    def __get_tweets(self):
        start_time = time.time()
        tweets_list = query_tweets(query=self.__hashtag, poolsize=1,
                                   lang=self.__lang, begindate=self.__from_date, enddate=self.__to_date)
        query_time = time.time() - start_time
        num_of_tweets = str(len(tweets_list))
        log_info("Took {0} to get {1} tweets".format(query_time, num_of_tweets))
        return tweets_list

    @staticmethod
    def __clean_tweets(tweets_list):
        start_time = time.time()
        tweets_list = [remove_quotation_mark(tweet) for tweet in tweets_list]
        cleaning_time = time.time() - start_time
        log_info("Took {0} to clean tweets".format(str(cleaning_time)))
        return tweets_list

    @staticmethod
    def __tweets_to_data_frame(tweets):  # TODO : Clean this please. One for loop is more than enough.
        df = pd.DataFrame(data=[remove_quotation_mark(tweet.text) for tweet in tweets], columns=['tweets'])
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

    @staticmethod
    def __remove_duplicates(tweets_df):
        start_time = time.time()
        tweets_df.drop_duplicates(subset=None, keep='first', inplace=True)
        dropping_duplicates_time = time.time() - start_time
        log_info("Took {0} to remove duplicates from tweets list".format(dropping_duplicates_time))
        return tweets_df

    @staticmethod
    def __get_highest_retweets(tweets_df, n):
        start_time = time.time()
        highest = tweets_df.nlargest(n, "retweets")
        highest_retweets_time = time.time() - start_time
        log_info("Took {0} to get highest retweets list".format(highest_retweets_time))
        return highest

    @staticmethod
    def __get_highest_likes(tweets_df, n):
        start_time = time.time()
        highest = tweets_df.nlargest(n, "likes")
        highest_likes_time = time.time() - start_time
        log_info("Took {0} to get highest likes list".format(highest_likes_time))
        return highest

    @staticmethod
    def get_highest_likes_and_retweets(tweets_df, n):
        start_time = time.time()
        highest = tweets_df.nlargest(n, "likes_and_retweets")
        highest_likes_and_retweets_time = time.time() - start_time
        log_info("Took {0} to get highest likes_and_retweets list".format(highest_likes_and_retweets_time))
        return highest

    @staticmethod
    def __sort_tweets(tweets_df):
        start_time = time.time()
        tweets_df.sort_values(by='likes_and_retweets', ascending=False, inplace=True, kind='quicksort',
                              na_position='last')
        sorting_time = time.time() - start_time
        log_info("Took {0} to sort tweets by date likes and retweets".format(sorting_time))
        return tweets_df

    def __write_and_upload_processed_tweets(self, cleaned_tweets) -> None:
        start_time = time.time()
        cleaned_tweets_file = open(self.__job_name + '.txt', 'w')
        [cleaned_tweets_file.write(tweet + '\n') for tweet in cleaned_tweets]
        upload_path = str(cleaned_tweets_file.name)
        cleaned_tweets_file.flush()
        cleaned_tweets_file.close()
        writing_time = time.time() - start_time
        upload_file_to_s3(upload_path)
        time.sleep(15)
        log_info("Took {0} to write and upload tweets to s3. Upload path {1}".format(writing_time, upload_path))


def remove_quotation_mark(text):
    return text.replace("\"", "'").replace("\n", "")
