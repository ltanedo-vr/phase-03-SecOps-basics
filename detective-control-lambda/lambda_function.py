import json
import os
import boto3


def lambda_handler(event, context):
    '''
    Sends config rule to AWS config, 
    checking if logging is enabled on all s3 buckets
    '''
    
    '''init boto3'''
    session = boto3.Session(
        aws_access_key_id    =os.environ["access"],
        aws_secret_access_key=os.environ["secret"]
    )
    
    '''init config client'''
    client = session.client('config')
    
    '''load config from json file'''
    config = json.loads(
        open("customRule.json", "r").read()
    )
    
    ''' put rule to aws config'''
    response = client.put_config_rule(
        ConfigRule= config
    )
    
    #TODO: Catch errors using Try,Except,Finally

    return {
        'statusCode': response["ResponseMetadata"]["HTTPStatusCode"],
        'body': response["ResponseMetadata"]
    }
