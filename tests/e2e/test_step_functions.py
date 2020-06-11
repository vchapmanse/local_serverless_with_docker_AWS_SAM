import boto3
import json
sfn = boto3.client(
    "stepfunctions",
    endpoint_url="http://127.0.0.1:8083")

DYDB = boto3.resource("dynamodb", endpoint_url="http://localhost:8000")

def test_code_of_conduct(s3_cloudwatch_event):
    event = s3_cloudwatch_event
    event["detail"]["resources"][0].update({"ARN": "arn:aws:s3:::code_of_conduct.txt"})
    resp = sfn.start_execution(
        stateMachineArn='arn:aws:states:us-east-1:123456789012:stateMachine:test_machine',
        input=json.dumps(event)
    )
    resp = sfn.describe_execution(
        executionArn=resp["executionArn"]
    )
    while resp.get("status") == "RUNNING":
        resp = sfn.describe_execution(
            executionArn=resp["executionArn"]
        )
        
    assert resp["status"] == 'SUCCEEDED'

def test_user_groups(s3_cloudwatch_event):
    event = s3_cloudwatch_event
    event["detail"]["resources"][0].update({"ARN": "arn:aws:s3:::user_groups.txt"})
    resp = sfn.start_execution(
        stateMachineArn='arn:aws:states:us-east-1:123456789012:stateMachine:test_machine',
        input=json.dumps(event)
    )
    resp = sfn.describe_execution(
        executionArn=resp["executionArn"]
    )
    while resp.get("status") == "RUNNING":
        resp = sfn.describe_execution(
            executionArn=resp["executionArn"]
        )
        
    assert resp["status"] == 'SUCCEEDED'

def test_event_description(s3_cloudwatch_event):
    event = s3_cloudwatch_event
    event["detail"]["resources"][0].update({"ARN": "arn:aws:s3:::event_description.txt"})
    with open('./state_machine.json', 'r') as myfile:
        data = myfile.read()

    try:
        sfn.create_state_machine(
            name='test_machine',
            definition=data,
            roleArn="arn:aws:iam::012345678901:role/DummyRole"
        )
    except Exception as e:
        print(e)
        pass
    resp = sfn.start_execution(
        stateMachineArn='arn:aws:states:us-east-1:123456789012:stateMachine:test_machine',
        input=json.dumps(event)
    )
    
    resp = sfn.describe_execution(
        executionArn=resp["executionArn"]
    )
    while resp.get("status") == "RUNNING":
        resp = sfn.describe_execution(
            executionArn=resp["executionArn"]
        )
        
    assert resp["status"] == 'SUCCEEDED'

def test_rejected_file(s3_cloudwatch_event):
    event = s3_cloudwatch_event
    event["detail"]["resources"][0].update({"ARN": "arn:aws:s3:::rejected_file.txt"})
    
    resp = sfn.start_execution(
        stateMachineArn='arn:aws:states:us-east-1:123456789012:stateMachine:test_machine',
        input=json.dumps(event)
    )
    resp = sfn.describe_execution(
        executionArn=resp["executionArn"]
    )
    while resp.get("status") == "RUNNING":
        resp = sfn.describe_execution(
            executionArn=resp["executionArn"]
        )
        
    assert resp["status"] == 'SUCCEEDED'