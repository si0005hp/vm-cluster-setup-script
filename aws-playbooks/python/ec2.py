import boto3

ec2_client = boto3.client('ec2')

ec2s = ec2_client.describe_instances(Filters=[
    {
        'Name': 'tag:Name',
        'Values': ['dev-log', 'dev-tunnel']
    },
])


def get_ec2_instance_ids(instance_names):
    ec2s = ec2_client.describe_instances(Filters=[
        {
            'Name': 'tag:Name',
            'Values': instance_names
        },
    ])
    return list(
        map(lambda r: r['Instances'][0]['InstanceId'], ec2s['Reservations']))


ids = get_ec2_instance_ids(['dev-log', 'dev-tunnel'])
res = ec2_client.stop_instances(InstanceIds=ids)
code = res['ResponseMetadata']['HTTPStatusCode']

print(type(code))
print(code)
