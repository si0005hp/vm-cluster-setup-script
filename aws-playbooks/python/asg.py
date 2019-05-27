import boto3
import os

asg_client = boto3.client('autoscaling')


def get_ap_asg_name():
    hits = list(
        filter(
            lambda asg: 'CodeDeploy_dev-ap-blue-green' in asg['AutoScalingGroupName'],
            asg_client.describe_auto_scaling_groups()['AutoScalingGroups']))

    if len(hits) < 1:
        return null
    else:
        return hits[0]['AutoScalingGroupName']


res = asg_client.describe_auto_scaling_groups(
    AutoScalingGroupNames=['dev-selenium-asg'])

print(res)
