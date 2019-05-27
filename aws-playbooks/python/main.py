import boto3
import os
import json

EC2_INSTANCE_NAMES = [
    'dev-log',
    'dev-tunnel',
]

RDS_CLUSTER_NAMES = 'dev-cluster'

asg_client = boto3.client('autoscaling')
ec2_client = boto3.client('ec2')
rds_client = boto3.client('rds')


def handleResponse(res):
    http_status_code = res['ResponseMetadata']['HTTPStatusCode']
    if http_status_code != 200:
        raise Exception(
            'Invalid http status code: {}'.format(http_status_code))
    else:
        print(res)


def get_ap_asg_name():
    hits = list(
        filter(
            lambda asg: 'CodeDeploy_dev-ap-blue-green' in asg['AutoScalingGroupName'],
            asg_client.describe_auto_scaling_groups()['AutoScalingGroups']))

    if len(hits) < 1:
        return None
    else:
        return hits[0]['AutoScalingGroupName']


def get_ec2_instance_ids(instance_names):
    ec2s = ec2_client.describe_instances(Filters=[
        {
            'Name': 'tag:Name',
            'Values': instance_names
        },
    ])
    return list(
        map(lambda r: r['Instances'][0]['InstanceId'], ec2s['Reservations']))


def get_rds_status(rds_cluster_name):
    return rds_client.describe_db_clusters(
        DBClusterIdentifier='dev-cluster')['DBClusters'][0]['Status']


def up():
    # ap-asg
    ap_asg_name = get_ap_asg_name()
    if ap_asg_name != None:
        res = asg_client.update_auto_scaling_group(
            AutoScalingGroupName=ap_asg_name, MinSize=1, DesiredCapacity=1)
        handleResponse(res)

    # selenium-asg
    res = asg_client.update_auto_scaling_group(
        AutoScalingGroupName='dev-selenium-asg', MinSize=3, DesiredCapacity=3)
    handleResponse(res)

    # other ec2 instances
    res = ec2_client.start_instances(
        InstanceIds=get_ec2_instance_ids(EC2_INSTANCE_NAMES))
    handleResponse(res)

    # RDS
    if get_rds_status(RDS_CLUSTER_NAMES) not in [
            'starting', 'stopping', 'available'
    ]:
        res = rds_client.start_db_cluster(
            DBClusterIdentifier=RDS_CLUSTER_NAMES)
        handleResponse(res)


def down():
    # ap-asg
    ap_asg_name = get_ap_asg_name()
    if ap_asg_name != None:
        res = asg_client.update_auto_scaling_group(
            AutoScalingGroupName=ap_asg_name, MinSize=0, DesiredCapacity=0)
        handleResponse(res)

    # selenium-asg
    res = asg_client.update_auto_scaling_group(
        AutoScalingGroupName='dev-selenium-asg', MinSize=0, DesiredCapacity=0)
    handleResponse(res)

    # other ec2 instances
    res = ec2_client.stop_instances(
        InstanceIds=get_ec2_instance_ids(EC2_INSTANCE_NAMES))
    handleResponse(res)

    # RDS
    if get_rds_status(RDS_CLUSTER_NAMES) not in [
            'starting', 'stopping', 'stopped'
    ]:
        res = rds_client.stop_db_cluster(DBClusterIdentifier=RDS_CLUSTER_NAMES)
        handleResponse(res)


def execute(op_type):
    if op_type == 'up':
        up()
    elif op_type == 'down':
        down()
    else:
        raise Exception(op_type)


def lambda_handler(event, context):
    try:
        op_type = event['op_type']
        execute(op_type)
        return {
            'statusCode': 200,
            'body': json.dumps('Success: {}'.format(op_type))
        }
    except Exception as e:
        print(e)
        raise e