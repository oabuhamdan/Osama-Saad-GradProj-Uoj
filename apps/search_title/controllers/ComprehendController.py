import boto3

from .Utils import log_info

comprehend_client = boto3.client(service_name='comprehend', region_name='us-east-1')


class SentimentAnalysisJob:
    __job_name = ''

    __job_status = ''
    __output_path = ''
    __job_id = ''
    __job_start_time = ''
    __job_finish_time = ''
    __lang = ''

    def __init__(self, job_name, lang):
        self.__job_name = job_name
        self.__lang = lang

    def create_and_start_new_job(self):
        response = self.__start_sa_job()
        self.__set_job_info(response)
        log_info("New sentiment analysis job has started, with the following info " + str(self.get_job_info()))

    def get_job_info(self):
        info = {
            "job_name": self.__job_name,
            "job_id": self.__job_id,
            "out_path": self.__output_path,
            "start_time": self.__job_start_time,
        }
        return info

    def __set_job_info(self, response):
        self.__job_id = response["JobId"]
        self.__set_job_status()
        self.__set_output_file_path()
        self.__set_start_time()

    def __start_sa_job(self):
        response = comprehend_client.start_sentiment_detection_job(
            InputDataConfig={
                'S3Uri': 's3://grad-proj-bucket/SA-Inputs/{0}.txt'.format(self.__job_name),
                'InputFormat': 'ONE_DOC_PER_LINE'
            },
            OutputDataConfig={
                'S3Uri': 's3://grad-proj-bucket/SA-Outputs/',
            },
            DataAccessRoleArn='arn:aws:iam::302740440137:role/service-role/AmazonComprehendServiceRoleS3FullAccess-SA_GradProj',
            JobName=self.__job_name,
            LanguageCode=self.__lang
        )
        return response

    def __set_job_status(self):
        self.__job_status = comprehend_client.describe_sentiment_detection_job(
            JobId=self.__job_id
        )

    def __set_output_file_path(self):
        self.__output_path = self.__job_status["SentimentDetectionJobProperties"]["OutputDataConfig"]["S3Uri"][22:]

    def __set_start_time(self):
        self.__job_start_time = self.__job_status["SentimentDetectionJobProperties"]["SubmitTime"]

    def __str__(self):
        return self.__job_name
