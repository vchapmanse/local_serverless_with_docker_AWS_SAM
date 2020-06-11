import pytest
import os
import boto3
import json

@pytest.fixture(scope="session", autouse=True)
def setup_environment():
    client = boto3.client(
        "s3",
        endpoint_url="http://127.0.0.1:9000",
        aws_access_key_id="AKIAIOSFODNN7EXAMPLE",
        aws_secret_access_key="wJalrXUtnFEMIK7MDENGbPxRfiCYEXAMPLEKEY")

    sfn = boto3.client(
        "stepfunctions",
        endpoint_url="http://127.0.0.1:8083")

    DYDB = boto3.resource("dynamodb", endpoint_url="http://localhost:8000")
    try:
        table = DYDB.create_table(
            TableName='WordCounts',
            KeySchema=[
                {
                    'AttributeName': 'primary_key',
                    'KeyType': 'HASH'
                },
                {
                    'AttributeName': 'sort_key',
                    'KeyType': 'RANGE'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'primary_key',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'sort_key',
                    'AttributeType': 'S'
                },
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
    except:
        pass

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

@pytest.fixture()
def s3_cloudwatch_event():
    with open('./tests/events/s3_test_event.json', 'r') as myfile:
        data = myfile.read()

    return json.loads(data)
