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
    remediationConfig = json.loads(
        open("remediation.json", "r").read()
    )
    
    ''' load Remediation into Config Rule '''
    response = client.put_remediation_configurations(
        RemediationConfigurations=remediationConfig
    )
    
    ''' Excecute Remediation '''
    response = client.start_remediation_execution(
        ConfigRuleName='s3-bucket-logging-enabled',
         ResourceKeys=[
            {
                'resourceType': 'AWS::S3::Bucket',
                'resourceId': 'config-bucket-057361781086'
            }
        ]
    )

    #TODO: Catch errors using Try,Except,Finally

    return {
        'statusCode': response["ResponseMetadata"]["HTTPStatusCode"],
        'body': response["ResponseMetadata"]
    }
