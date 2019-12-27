import json
import boto3
from datetime import datetime, timedelta

def main():
  cloudwatch_client = boto3.client('cloudwatch')

  now = datetime.now()
  ten_min_ago = now - timedelta(minutes=10)

  response = cloudwatch_client.get_metric_statistics(
      Namespace='AWS/RDS',
      MetricName='CPUUtilization',
      StartTime=ten_min_ago,
      EndTime=now,
      Period=600,
      Statistics=['Maximum'],
  )

  max = 0
  for e in response['Datapoints']:
    if e['Maximum'] > max:
      max = e['Maximum']

  res = {
    'period': '{0} ~ {1}'.format(ten_min_ago.strftime("%Y/%m/%d %H:%M:%S"), now.strftime("%Y/%m/%d %H:%M:%S")),
    'max_cpuutilization': max
  }

  return res


def lambda_handler(event, context):
    
    print(main())

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
