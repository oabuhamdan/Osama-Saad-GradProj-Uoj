import json

import boto3

s3_client = boto3.client('s3')
my_bucket = "grad-proj-bucket"


def get_results_from_bucket(output_path):
    response = s3_client.select_object_content(
        Bucket=my_bucket,
        Key=output_path,
        Expression='select s.line,s.sentiment,s.SentimentScore from s3object[*] s where s.line is not missing',
        ExpressionType='SQL',
        RequestProgress={
            'Enabled': True
        },
        InputSerialization={
            'CompressionType': 'GZIP',
            'JSON': {
                'Type': 'Lines'
            }
        },
        OutputSerialization={
            'JSON': {
                'RecordDelimiter': ','
            }
        }
    )
    return response


def get_sa_results_as_json(output_path):
    response = get_results_from_bucket(output_path)
    results = ""
    event_stream = response['Payload']
    end_event_received = False
    with open('output', 'wb') as f:
        # Iterate over events in the event stream as they come
        for event in event_stream:
            # If we received a records event, write the data to a file
            if 'Records' in event:
                data = event['Records']['Payload']
                results += bytes(data).decode('utf-8')
                end_event_received = True
    if not end_event_received:
        raise Exception("End event not received, request incomplete.")

    result = '{\"Results' + '\":[' + results[:-1] + ']}'
    return json.loads(result)


def download_file_from_s3(file_path):
    s3_client.download_file(my_bucket, file_path, "/home/osama-hamdan/Downloads/out.txt")


def upload_file_to_s3(file_name):
    s3_client.upload_file(file_name, my_bucket, 'SA-Inputs/' + file_name)
