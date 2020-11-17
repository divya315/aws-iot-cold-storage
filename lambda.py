import json
import boto3

sns = boto3.client('sns')
iot=boto3.client('iot-data')

def lambda_handler(event, context):
    print(event)
    res=event['current']['state']['reported']['airConditioningIsOn']
    print(res)
    if(res==True):
        msg="Temperature is high,Air Conditioner is turned On"
    else:
        msg="It has become cold.Air Conditioner is turned Off"
    resp = sns.publish(TopicArn='arn:aws:sns:us-east-1:679306712123:tempcontroller',Message=msg,)
