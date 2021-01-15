from django.contrib.auth.decorators import user_passes_test, login_required
from django.http import HttpResponse
from django.shortcuts import render

from .controllers.ComprehendHelper import get_sentiment_result_for_top_tweets
from .controllers.OmdbController import get_movie_info
from .models import Title, Job, Result
from .controllers.TwitterScrapperController import *
from .controllers.JobHandler import *
from .controllers.Utils import convert_to_hashtag, get_date, get_next_date, get_URL, parse_tweets, get_top_tweets_json, \
    parse_tweets_json
from .controllers.DataBaseController import PostgresConnection
import datetime as dt

db = PostgresConnection()
languages = ["en", "ar", "es", "ja", "pt", "ko"]


def index(request):
    global db
    titles = db.get_all_from_titles()
    return render(request, "index.html", {"titles": titles})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def render_search(request):
    return render(request, "search.html")


def render_result(request):
    search_title = request.GET["search_title"]
    year = request.GET["year"]
    json_resp = get_movie_info(search_title, year)
    hashtag = convert_to_hashtag(json_resp["Title"])
    ratings = Ratings(json_resp['Ratings'][0]['Value'],
                      json_resp['Ratings'][1]['Value'],
                      json_resp['Ratings'][2]['Value'])
    if json_resp['Response'] == 'False':
        return HttpResponse("no result :( ")
    else:
        title = db.get_title_by_name_and_year(json_resp["Title"], json_resp["Year"])
        tweets = []
        results = []
        for language in languages:
            job_name = clean(hashtag) + "_" + year + "_" + language + "_Job"
            results.append(db.get_results(job_name))
            tweets.append(parse_tweets_json(db.get_tweets_by_job_name(job_name)))
        results = Results(results[0], results[1], results[2], results[3], results[4], results[5])
        tweets = Tweets(tweets[0], tweets[1], tweets[2], tweets[3], tweets[4], tweets[5])
        context = Context(tweets, title, results, None, ratings)
    return render(request, "result.html", {"context": context})


def search(request):
    global db
    search_title = request.GET["search_title"]
    year = request.GET["year"]
    json_resp = get_movie_info(search_title, year)
    hashtag = convert_to_hashtag(json_resp["Title"])
    ratings = json_resp["Ratings"]
    if json_resp['Response'] == 'False':
        return HttpResponse("no result :( ")
    else:
        title = db.get_title_by_name_and_year(json_resp["Title"], json_resp["Year"])
        if title is None:  # if title does not exist
            title = Title.create(name=json_resp["Title"], year=json_resp["Year"], released=json_resp["Released"],
                                 genre=json_resp["Genre"],
                                 director=json_resp["Director"], writer=json_resp["Writer"],
                                 actors=json_resp["Actors"],
                                 plot=json_resp["Plot"],
                                 lang=json_resp["Language"], poster=json_resp["Poster"],
                                 url=get_URL(search_title, year),
                                 latest_job_date=str(dt.date.today()))
            title.save()
            for language in languages:
                job_name = clean(hashtag) + "_" + year + "_" + language + "_Job"

                # create_scrapping_and_analysis_job(clean(json_resp["Title"]), year, hashtag, dt.date(2015, 1, 1),
                #                                   dt.date(2015, 1, 2), language)
                scrapping_job = ScrappingJob(hashtag=hashtag,
                                             job_name=job_name,
                                             from_date=get_date(json_resp["Released"]),
                                             to_date=dt.date.today(),
                                             lang=language)

                # all_tweets, top_tweets = scrapping_job.create_and_start_new_job()
                scrapping_job.create_and_start_new_job()
                # threading.Thread(target=scrapping_job.create_and_start_new_job, args=()).start()
                # top_tweets, top_tweets_json = get_top_tweets_json(top_tweets)
                # top_tweets_results = get_sentiment_result_for_top_tweets()
                time.sleep(5)
                sa = SentimentAnalysisJob(job_name=job_name, lang=language)
                sa.create_and_start_new_job()
                job_info = sa.get_job_info()
                job = Job.create(job_name=job_name, job_id=job_info['job_id'], start_time=job_info['start_time'],
                                 results_output_path=job_info['out_path'], sentiments_count="0", job_done=False)
                job.save()
            return HttpResponse("waiting for SA to finish..")
        else:  # if title exists
            for language in languages:
                job_name = clean(hashtag) + "_" + year + "_" + language + "_Job"
                job_results = db.get_results(job_name)
                if job_results is None:
                    return HttpResponse("waiting for SA to finish..")
                # title = db.get_title_by_job_name(job_name)
                db.set_job_done(job_name)
                db.update_sentiments_count(job_name, job_results.total)
                top_tweets = parse_tweets_json(db.get_tweets_by_job_name(job_name))
                top_tweets_text = []
                for tweet in top_tweets:
                    top_tweets_text.append(tweet.text)
                top_tweets_results = get_sentiment_result_for_top_tweets(top_tweets_text, language)
                for tweet, sentiment_result in zip(top_tweets, top_tweets_results):
                    tweet.set_sentiment_results(sentiment_results=sentiment_result)
    context = Context(top_tweets, title, job_results, top_tweets_results, None)
    return render(request, "result.html", {"context": context})


class Context:
    def __init__(self, tweets, title, result, sentiments, ratings):
        self.tweets = tweets
        self.title = title
        self.result = result
        self.sentiments = sentiments
        self.ratings = ratings


class Results:
    def __init__(self, en, ar, es, ja, pt, ko):
        self.en = en
        self.ar = ar
        self.es = es
        self.ja = ja
        self.pt = pt
        self.ko = ko
        self.total = self.__calculate_total()

    def __calculate_total(self):
        total_positive = (float(self.en.positive) + \
                          float(self.ar.positive) + \
                          float(self.es.positive) + \
                          float(self.ja.positive) + \
                          float(self.ko.positive) + \
                          float(self.pt.positive)) / 6
        total_negative = (float(self.en.negative) + \
                          float(self.ar.negative) + \
                          float(self.es.negative) + \
                          float(self.ja.negative) + \
                          float(self.ko.negative) + \
                          float(self.pt.negative)) / 6
        total_neutral = (float(self.en.neutral) + \
                         float(self.ar.neutral) + \
                         float(self.es.neutral) + \
                         float(self.ja.neutral) + \
                         float(self.ko.neutral) + \
                         float(self.pt.neutral)) / 6
        total_sentiments = (int(self.en.total) + \
                            int(self.ar.total) + \
                            int(self.es.total) + \
                            int(self.ja.total) + \
                            int(self.ko.total) + \
                            int(self.pt.total))
        total_result = Result.create("None", str(total_positive), str(total_negative), str(total_neutral),
                                     str(total_sentiments))
        return total_result


class Ratings:
    def __init__(self, imdb, rt, mc):
        self.imdb = imdb
        self.rt = rt
        self.mc = mc


class Tweets:
    def __init__(self, en, ar, es, ja, pt, ko):
        self.en = en
        self.ar = ar
        self.es = es
        self.ja = ja
        self.pt = pt
        self.ko = ko
