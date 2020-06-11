import boto3
import os
import json

if os.environ.get("AWS_SAM_LOCAL"):
    URL = "http://docker.for.mac.localhost:8083"
else:
    URL = None

sfn = boto3.client(
    "stepfunctions",
    endpoint_url=URL)

def lambda_handler(event, context) -> None:
    """
    Notifies users of a manual approval required.
    """
    resources = event['ExecutionContext']["Execution"]["Input"]["detail"]["resources"]
    for resource in resources:
        if "Object" in resource["type"]:
            object_arn = resource["ARN"]
            break

    if "rejected" in object_arn:
        status = "Rejected!"
    else:
        status = "Approved!"

    sfn.send_task_success(
        taskToken=event["ExecutionContext"]["Task"]["Token"],
        output=json.dumps({"Status": status})
    )
    
    return