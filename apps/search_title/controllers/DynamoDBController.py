import boto3

dynamodb = boto3.resource('dynamodb')


def write_to_db(table_name, data):
    dynamodb.put_item(
        TableName=table_name,
        Item=data
    )


def write_movie_info_to_db(movie_info):
    table_name = 'Movies_Info'
    movie_info_json = {
        'movie_name': movie_info['Title'] + '_' + movie_info['Year'],
        'release_date': movie_info['Released'],
        'poster': movie_info['Poster'],
        'imdb_rating': movie_info['imdbRating'],
        'imdb_votes': movie_info['imdbVotes'],
        'rotten_tomatoes_rating': movie_info['Ratings'][1]["Value"],
        'meta_critic_rating': movie_info['Ratings'][2]["Value"],
        'meta_score_rating': movie_info['Metascore']
    }
    write_to_db(table_name, movie_info_json)


def write_job_info_to_db(job_info):
    table_name = 'SA_Jobs_Info'
    job_info_json = {
        'movie_name': job_info['job_name'],
        'job_id': job_info['job_id'],
        'start_time': job_info['start_time'],
        'end_time': job_info['end_time'],
        'results_output_path': job_info['output_path'],
        'sentiments_count': job_info['sentiments_count'],
        'positive_count': job_info['positive_count'],
        'negative_count': job_info['negative_count'],
        'mixed_count': job_info['mixed_count']
    }
    write_to_db(table_name, job_info_json)


def write_tweets_info(tweets_info):
    table_name = 'Tweets_Info'
    tweets_info_json = {
        'movie_name': tweets_info['movie_name'],
        'used_hash_tags': tweets_info['used_hash_tags'],
        'tweets_count': tweets_info['tweets_count'],
        'most_liked_tweets': tweets_info['most_liked_tweets'],
        'most_retweeted_tweets': tweets_info['most_retweeted_tweets']
    }
    write_to_db(table_name, tweets_info_json)
