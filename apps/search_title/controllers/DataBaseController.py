import psycopg2

from ..controllers.JobHandler import get_job_results_if_done
from ..models import *
from .Utils import *


class PostgresConnection:
    __connection_with_db = None
    __cursor = None
    __is_connected = False

    def __connect(self):

        self.__connection_with_db = psycopg2.connect(host="127.0.0.1",
                                                     database="my_database",
                                                     user="postgres",
                                                     password="saadjal")
        self.__cursor = self.__connection_with_db.cursor()
        self.__is_connected = True

    def __disconnect(self):
        if self.__is_connected:
            self.__connection_with_db.close()
            self.__cursor.close()
            self.__is_connected = True
        else:
            raise ConnectionError("not connected to data base to close")

    def get_all_from_titles(self):
        self.__connect()
        self.__cursor.execute("SELECT * FROM search_title_title ")
        rows = self.__cursor.fetchall()
        titles = []
        for id, name, poster, year, actors, director, genre, lang, plot, released, writer,  url, latest_job_date in rows:
            titles.append(Title.create(name, year, released, genre, director, writer, actors, plot, lang, poster,
                                        url, latest_job_date))
        self.__disconnect()
        return titles

    def get_title_by_name_and_year(self, name, year):
        self.__connect()
        self.__cursor.execute("SELECT * FROM search_title_title WHERE (name = %s AND year = %s)",
                              (name, year))
        rows = self.__cursor.fetchall()
        title = None
        if not rows:  # not in db
            self.__disconnect()
            return None
        else:
            for id, name, poster, year, actors, director, genre, lang, plot, released, writer, url, latest_job_date in rows:
                title = Title.create(name, year, released, genre, director, writer, actors, plot, lang, poster,
                                     url, latest_job_date)
            self.__disconnect()
            return title

    def get_title_by_job_name(self, job_name):
        self.__connect()
        self.__cursor.execute("SELECT * FROM search_title_title WHERE (job_name = %s)",
                              (job_name,))
        rows = self.__cursor.fetchall()
        title = None
        if not rows:  # not in db
            self.__disconnect()
            return None
        else:
            for id, name, poster, year, actors, director, genre, lang, plot, released, writer, url, latest_job_date in rows:
                title = Title.create(name, year, released, genre, director, writer, actors, plot, lang, poster
                                     , url, latest_job_date)
            self.__disconnect()
            return title

    def set_job_done(self, job_name):
        self.__connect()
        self.__cursor.execute("UPDATE search_title_job SET job_done = TRUE WHERE job_name = %s", (job_name,))
        self.__connection_with_db.commit()
        self.__disconnect()

    def update_sentiments_count(self, job_name, sentiments_count):
        self.__connect()
        self.__cursor.execute("UPDATE search_title_job SET sentiments_count = %s WHERE job_name = %s",
                              (sentiments_count, job_name))
        self.__connection_with_db.commit()
        self.__disconnect()

    def get_tweets_from_title(self, name, year):
        self.__connect()
        self.__cursor.execute("SELECT tweets FROM search_title_title WHERE (name = %s AND year = %s)",
                              (name, year))
        rows = self.__cursor.fetchall()
        self.__disconnect()
        return parse_tweets(rows[0][0])

    def get_results(self, job_name):
        self.__connect()
        self.__cursor.execute("SELECT * FROM search_title_result WHERE job_name = %s",
                              (job_name,))
        rows = self.__cursor.fetchall()
        result = None
        if not rows:
            job_results = get_job_results_if_done(job_name)
            if job_results is not None:
                result = Result.create(job_name, job_results['positive'],
                                       job_results['negative'],
                                       job_results['neutral'],
                                       job_results['total'])
                result.save()
        else:
            for id, job_name, negative, neutral, positive, total in rows:
                result = Result.create(job_name, positive, negative, neutral, total)
        self.__disconnect()
        return result

    def get_job_id(self, job_name):
        self.__connect()
        self.__cursor.execute("SELECT job_id FROM search_title_job WHERE (job_name = %s)", (job_name,))
        row = self.__cursor.fetchall()
        self.__disconnect()
        return row[0][0]

    def get_output_path(self, job_name):
        self.__connect()
        self.__cursor.execute("SELECT results_output_path FROM search_title_job WHERE (job_name = %s)", (job_name,))
        row = self.__cursor.fetchall()
        self.__disconnect()
        return row[0][0]

    def get_tweets_by_job_name(self, job_name):
        self.__connect()
        self.__cursor.execute("SELECT text from search_title_toptweet WHERE job_name = %s",
                              (job_name,))
        row = self.__cursor.fetchall()
        self.__connection_with_db.commit()
        self.__disconnect()
        return row[0][0]
