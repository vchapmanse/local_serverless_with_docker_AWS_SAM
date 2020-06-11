import boto3
import os
import json

if os.environ.get("AWS_SAM_LOCAL"):
    URL = "http://docker.for.mac.localhost:9000"
    ACCESS_KEY = "wJalrXUtnFEMIK7MDENGbPxRfiCYEXAMPLEKEY"
    KEY_ID = "AKIAIOSFODNN7EXAMPLE"
else:
    URL = None
    ACCESS_KEY = None
    KEY_ID = None

S3_CLIENT = boto3.client(
    "s3",
    endpoint_url=URL,
    aws_access_key_id=KEY_ID,
    aws_secret_access_key=ACCESS_KEY)

def get_file(object_key, bucket):
    """
    Retrieves the file contents from S3.
    """
    resp = S3_CLIENT.get_object(
        Bucket=bucket,
        Key=object_key
    )
    read = resp['Body'].read()
    return read.decode('utf-8')
