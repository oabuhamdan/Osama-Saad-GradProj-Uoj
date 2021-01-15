from django.db import models


# Create your models here.

class Title(models.Model):
    name = models.TextField()
    year = models.IntegerField()
    released = models.TextField()
    genre = models.TextField()
    director = models.TextField()
    writer = models.TextField()
    actors = models.TextField()
    plot = models.TextField()
    lang = models.TextField()
    poster = models.TextField()
    url = models.TextField()
    latest_job_date = models.TextField()

    @classmethod
    def create(cls, name, year, released, genre, director, writer, actors, plot, lang, poster,
               url, latest_job_date):
        title = cls(name=name, year=year, released=released, genre=genre, director=director, writer=writer,
                    actors=actors, plot=plot, lang=lang, poster=poster, url=url, latest_job_date=latest_job_date)
        return title

    def __str__(self):
        return "name : " + str(self.name) + " year : " + str(self.year) + " released : " + str(
            self.released) + " genre : " + str(self.genre) + " director : " + str(self.director) + " writer : " + str(
            self.writer) + " actors : " + str(self.actors) + " plot : " + str(self.plot) + " lang : " + str(
            self.lang) + " poster : " + str(self.poster) + " tweets : " + " job_done : " + " url : " + str(
            self.url) + " latest_job_date : " + str(self.latest_job_date)


class Job(models.Model):
    job_name = models.TextField()
    job_id = models.TextField()
    start_time = models.TextField()
    results_output_path = models.TextField()
    sentiments_count = models.TextField()
    job_done = models.BooleanField()

    @classmethod
    def create(cls, job_name, job_id, start_time, results_output_path, sentiments_count, job_done):
        job = cls(job_name=job_name, job_id=job_id, start_time=start_time,
                  results_output_path=results_output_path, sentiments_count=sentiments_count, job_done=job_done)
        return job

    def __str__(self):
        return self.job_name


class Result(models.Model):
    job_name = models.TextField()
    positive = models.TextField()
    negative = models.TextField()
    neutral = models.TextField()
    total = models.TextField()

    # TODO job_id = models.ForeignKey(Job) for now I'll use job_name

    @classmethod
    def create(cls, job_name, positive, negative, neutral, total):
        job = cls(job_name=job_name, positive=positive, negative=negative, neutral=neutral, total=total)
        return job

    def __str__(self):
        return self.job_name


class TopTweet(models.Model):
    text = models.TextField()
    job_name = models.TextField()

    @classmethod
    def create(cls, text, job_name):
        job = cls(text=text, job_name=job_name)
        return job

    def __str__(self):
        return str(self.job_name) + "\n" + str(self.text)


class Tweet:
    text: str
    tweet_id: str
    user_id: str
    username: str
    screen_name: str
    len: str
    date: str
    likes: str
    retweets: str
    likes_and_retweets: str

    def __init__(self, text, tweet_id, user_id, username, screen_name, len, date, likes, retweets,
                 likes_and_retweets):
        self.text = text
        self.tweet_id = tweet_id
        self.user_id = user_id
        self.username = username
        self.screen_name = screen_name
        self.len = len
        self.date = date
        self.likes = likes
        self.retweets = retweets
        self.likes_and_retweets = likes_and_retweets
        self.sentiment = ''
        self.mixed = ''
        self.negative = ''
        self.neutral = ''
        self.positive = ''

    def set_sentiment_results(self, sentiment_results):
        self.sentiment = sentiment_results['Sentiment']
        self.mixed = sentiment_results['Mixed']
        self.negative = sentiment_results['Negative']
        self.neutral = sentiment_results['Neutral']
        self.positive = sentiment_results['Positive']

    def __str__(self):
        return "text : " + self.text + "tweet_id : " \
               + self.tweet_id + "user_id : " + self.user_id \
               + "username : " + self.username + "screen_name : " + self.screen_name \
               + "len : " + self.len + "date : " + self.date + \
               "likes : " + self.likes + "retweets : " + self.retweets + \
               "likes_and_retweets : " + self.likes_and_retweets
