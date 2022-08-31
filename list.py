import boto3
import logging
import os
from tabulate import tabulate
import argparse

ec2_instances = []
volume_sizes = []
GiB_TO_GB_UNIT = 1.073741824


# Get capacity of attached volumes in GB
def get_attached_volume_size(instances, ec2):
    describedVolumes = ec2.describe_volumes(
        Filters=[{'Name':'attachment.instance-id',
        'Values':[instances['InstanceId']]}]
    )

    totalEbsVolumeInInstanceSize = 0
    
    for volume in (describedVolumes["Volumes"]):
        totalEbsVolumeInInstanceSize += (volume["Size"])
    
    return totalEbsVolumeInInstanceSize * GiB_TO_GB_UNIT

# Helper function used to validate input
def check_defined(reference, reference_name):
    if not reference:
        raise Exception('Error: ', reference_name, 'is not defined')
    return reference

def get_server_by_name(client, name):
    return client.describe_instances(
        Filters=[{
            'Name': 'tag:Name',
            'Values': [name]
        }]
    )

def get_all_servers(client):
    return client.describe_instances()

def sort_instances_by_volume_size(instances):
    return sorted(instances, key=lambda i: i['VolumeSize'], 
        reverse=True)

def lambda_handler(event, context):
    logging.basicConfig(level=logging.ERROR)

    try:
        logging.info("-----------EC2 Instance(s) Description------------")

        region = 'eu-central-1'
        environment = os.getenv('ENVIRONMENT')

        if 'local' ==  environment:
            awsProfile = os.getenv('PROFILE')
            if not awsProfile: 
                awsProfile = 'default'
            session = boto3.Session(profile_name=awsProfile, region_name=region)
        else:  
            session = boto3.Session(region_name=region)
        
        check_defined(event, 'event')
        filter = event['filter']
        ec2_client = session.client('ec2')

        if '*' == filter:
            reservations = get_all_servers(ec2_client)
        else:
            reservations = get_server_by_name(ec2_client, filter)

        for reservation in reservations['Reservations']:
            for instance in reservation['Instances']:
                volumeSize = get_attached_volume_size(instance, ec2_client)
                volume_sizes.append(volumeSize)

                ec2_instances.append({
                    'InstanceId': instance.get('InstanceId', ''),
                    'InstanceType': instance.get('InstanceType', ''),
                    'State': instance['State']['Name'],
                    'PublicIp': instance.get('PublicIpAddress', ''),
                    'PrivateIp': instance.get('PrivateIpAddress', ''),
                    'SubnetId': instance.get('SubnetId', ''),
                    'VpcId': instance.get('VpcId', ''),
                    'VolumeSize': volumeSize           
                    })
        
        sorted_instances = sort_instances_by_volume_size(ec2_instances)
        
        print(tabulate(sorted_instances, headers="keys"))

        total_of_all_server_volumes = sum(volume_sizes)
        print(f'Total volume across all servers: {total_of_all_server_volumes:.2f} GB')

    except Exception as e:
        logging.exception(
            'Task failed with exception: {}'.format(e)
        )

if __name__ == '__main__': 
    parser = argparse.ArgumentParser(description='Get description of EC2 instances and associated EBS volumes')
    parser.add_argument('filter', nargs='?', default='*', help='Pass in wildcard or name of instance')
    args = parser.parse_args()

    event = {}
    event['filter'] = args.filter
    lambda_handler(event, None)