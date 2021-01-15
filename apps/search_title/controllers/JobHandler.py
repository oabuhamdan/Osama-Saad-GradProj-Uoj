import os
from multiprocessing.pool import ThreadPool
from queue import Queue
from .ComprehendController import SentimentAnalysisJob
from .TwitterScrapperController import ScrappingJob
from .Utils import log_info
from . import ComprehendHelper

cpu_count = os.cpu_count()
pool = ThreadPool(processes=cpu_count - 1)
queue_of_jobs = Queue()


def create_scrapping_and_analysis_job(movie_title, movie_release_year, hashtag, from_date, to_date, lang):
    job_name = movie_title + '_' + movie_release_year
    twitter_scrapping_job = ScrappingJob(hashtag, job_name, from_date, to_date, lang)
    sentiment_analysis_job = SentimentAnalysisJob(job_name, lang)
    scraping_and_analysis_job = {'ScrappingJob': twitter_scrapping_job, 'AnalysisJob': sentiment_analysis_job}
    pool.apply_async(start_job, args=(scraping_and_analysis_job, job_name))
    log_info("Scrapping and Analysis job has scheduled, with the following info " + str(job_name))


def start_job(job, job_name):
    job["ScrappingJob"].create_and_start_new_job()
    log_info("Scrapping job has started for " + str(job_name))
    job["AnalysisJob"].create_and_start_new_job()
    log_info("Analysis job has started for " + str(job_name))


def get_job_results_if_done(job_name):
    is_done = ComprehendHelper.is_job_done(job_name)

    if is_done:
        log_info('Job with name {0} was done at {1}'.format(job_name, 'time'))
        return ComprehendHelper.get_job_results(job_name)
    else:
        return None
