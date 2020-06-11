import os
import boto3

if os.environ.get("AWS_SAM_LOCAL"):
    URL = "http://docker.for.mac.localhost:8000"
else:
    URL = None

DYDB = boto3.resource("dynamodb", endpoint_url=URL)
TABLE = DYDB.Table("WordCounts")

def create_file(object_key, word_count):
    """
    Creates the originial record in dynamodb.
    """
    try:
        TABLE.put_item(
            Item={
                "primary_key": object_key,
                "word_counts": word_count,
                "sort_key": "Record"
            }
        )
    except:
        print(object_key)
        print(word_count)
        raise
