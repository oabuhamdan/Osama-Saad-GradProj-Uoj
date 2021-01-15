import boto3
import psycopg2

from .S3Helper import get_sa_results_as_json
from .Utils import log_info
import json
comprehend_client = boto3.client(service_name='comprehend', region_name='us-east-1')


def is_job_done(job_name):
    connection_with_db = psycopg2.connect(host="127.0.0.1",
                                          database="my_database",
                                          user="postgres",
                                          password="saadjal")
    cursor = connection_with_db.cursor()
    cursor.execute("SELECT job_id FROM search_title_job WHERE (job_name = %s)", (job_name,))
    row = cursor.fetchall()
    job_id = row[0][0]
    response = comprehend_client.describe_sentiment_detection_job(
        JobId=job_id
    )
    return response['SentimentDetectionJobProperties']['JobStatus'] == 'COMPLETED'


def get_job_results(job_name):
    connection_with_db = psycopg2.connect(host="127.0.0.1",
                                          database="my_database",
                                          user="postgres",
                                          password="saadjal")
    cursor = connection_with_db.cursor()

    cursor.execute("SELECT results_output_path FROM search_title_job WHERE (job_name = %s)", (job_name,))
    row = cursor.fetchall()
    output_path = row[0][0]
    s3_results = get_sa_results_as_json(output_path)
    results = {
        'POSITIVE': 0,
        'NEGATIVE': 0,
        'MIXED': 0,
        'NEUTRAL': 0,
        'TOTAL': 0,
    }

    for line in s3_results['Results']:
        results[line['sentiment']] += 1
        results['TOTAL'] += 1

    log_info('Calculating result for job {0} took {1}'.format(job_name, 'time'))
    cursor.close()
    connection_with_db.close()
    return calculate_results(results)


def calculate_results(results_json):
    positive_percentage = results_json['POSITIVE'] / results_json['TOTAL']
    negative_percentage = results_json['NEGATIVE'] / results_json['TOTAL']
    neutral_percentage = results_json['NEUTRAL'] / results_json['TOTAL']
    return {
        'positive': positive_percentage,
        'negative': negative_percentage,
        'neutral': neutral_percentage,
        'total': results_json['TOTAL'],
    }


def get_sentiment_result_for_top_tweets(top_tweets_list, lang):
    response = comprehend_client.batch_detect_sentiment(
        TextList=top_tweets_list,
        LanguageCode=lang
    )
    results = []
    for result in response['ResultList']:
        results.append(
            {
                'Sentiment': str(result['Sentiment']),
                'Mixed': str(result['SentimentScore']['Mixed']),
                'Negative': str(result['SentimentScore']['Negative']),
                'Neutral': str(result['SentimentScore']['Neutral']),
                'Positive': str(result['SentimentScore']['Positive'])
            }
        )
    return results







