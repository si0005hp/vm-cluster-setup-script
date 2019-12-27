import boto3
from datetime import datetime, timedelta

def main():
  cloudwatch_client = boto3.client('cloudwatch')

  now = datetime.now()
  ten_min_ago = now - timedelta(minutes=10)
  # now = now - timedelta(hours=9)
  # ten_min_ago = ten_min_ago - timedelta(hours=9)

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

  jst_from = (ten_min_ago + timedelta(hours=9)).strftime("%Y/%m/%d %H:%M:%S")
  jst_to = (now + timedelta(hours=9)).strftime("%Y/%m/%d %H:%M:%S")
  res = {
    'period': '{0} ~ {1}'.format(jst_from, jst_to),
    'max_cpuutilization': max
  }

  return res

print(str(main()))