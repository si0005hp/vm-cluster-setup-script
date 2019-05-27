import boto3

rds_client = boto3.client('rds')


def get_rds_status(rds_cluster_name):
    return rds_client.describe_db_clusters(
        DBClusterIdentifier='dev-cluster')['DBClusters'][0]['Status']


# print(get_rds_status('dev-cluster'))

res = rds_client.start_db_cluster(DBClusterIdentifier='dev-cluster')
print(res)