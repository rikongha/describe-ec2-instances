import boto3
import logging
import os


ec2_instances = []
volume_sizes=[]

# Get capacity of attached volumes in GB
def get_attached_volume_size(instances, ec2):
    describedVolumes = ec2.describe_volumes(
        Filters=[{'Name':'attachment.instance-id',
        'Values':[instances['InstanceId']]}]
    )

    volumeSize = 0
    GiB_TO_GB = 1.073741824
    for volume in (describedVolumes["Volumes"]):
        volumeSize += (volume["Size"])

    return volumeSize * GiB_TO_GB

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

def sort_by_size():
    return #TODO sort results


def lambda_handler(event, context):
    logging.basicConfig(level=logging.ERROR)

    try:
        logging.info("-----------EC2 Instance Description------------")

        # check_defined()
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
            # TODO get input from events and call appropriate fn


        ec2_client = session.client('ec2')

        reservations = get_server_by_name(ec2_client, 'jenkins')


        for reservation in reservations["Reservations"]:
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
                    'volume.size': volumeSize           
                    })
                    
        # TODO Print result to console  in tabular format
        header = ['instance-id', 'instance-type', 'status', 'private-ip', 'PublicIp', 
            'public-ip', 'total-size-ebs-volumes']
        
        total_of_all_server_volumes = sum(volume_sizes)
        print(f'Total volume across all servers: {total_of_all_server_volumes:.2f} GB')

    except Exception as e:
        logging.exception(
            'Task failed with exception: {}'.format(e)
        )

if __name__ == '__main__': 
    lambda_handler(None, None)