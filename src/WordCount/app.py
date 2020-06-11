from helpers import dynamodb_helpers
from helpers import s3_helpers
import os

def lambda_handler(event, context) -> None:
    """
    Takes a cloudwatch event and count the words of the provided s3 file.
    """
    resources = event["detail"]["resources"]
    word_count = {}
    for resource in resources:
        if "Object" in resource["type"]:
            object_arn = resource["ARN"]
        elif "Bucket" in resource["type"]:
            bucket_arn = resource["ARN"]


    bucket = bucket_arn.split(":")[-1]
    object_key = object_arn.split(":")[-1]

    file_contents = s3_helpers.get_file(object_key, bucket)

    words = file_contents.split(" ")
    for word in words:
        if not word:
            continue
        
        if word_count.get("word"):
            word_count[word] += 1
        else:
            word_count[word] = 1
    
    dynamodb_helpers.create_file(object_key, word_count)
    
    resp = {
        "Status": "Approved!",
        "words": list(word_count.keys()),
        "file_name": object_key
    }
    return resp
