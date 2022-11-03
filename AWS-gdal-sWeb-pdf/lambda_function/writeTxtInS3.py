
import json, boto3

def lambda_handler(event, context):

    string = "dfghj"
    # encoded_string = string.encode("utf-8")

    bucket_name = "josee-bucket3"

    file_name = "my_test.txt"
    s3_path = "output/" + file_name
    tmp_file = "/tmp/" + file_name

    with open(tmp_file, "w") as file:
        file.write(string)


    ## os.system('echo testing... >'+lambda_path)
    s3 = boto3.resource("s3")
    s3.meta.client.upload_file(tmp_file, bucket_name, file_name)

    # bucket_name = "s3bucket"
    # file_name = "hello.txt"
    # s3_path = "100001/20180223/" + file_name

    # s3 = boto3.resource("s3")
    # s3.Bucket(bucket_name).put_object(Key=s3_path, Body=encoded_string)
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }


import json, boto3,os, sys, uuid
from urllib.parse import unquote_plus

s3_client = boto3.client('s3')

def lambda_handler(event, context):
    some_text = "test"

    bucket_name = "josee-bucket3"
    file_name = "my_test_file.csv"
    lambda_path = "/tmp/" + file_name
    s3_path = "output/" + file_name
    os.system('echo testing... >'+lambda_path)
    s3 = boto3.resource("s3")
    s3.meta.client.upload_file(lambda_path, bucket_name, file_name)

    return {
        'statusCode': 200,
        'body': json.dumps('file is created in:'+s3_path)
    }
