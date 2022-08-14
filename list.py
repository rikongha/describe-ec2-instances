import boto3
from tabulate import tabulate
from dotenv import load_dotenv
import os

# Load credentials
load_dotenv()
access_key = os.getenv('ACCESS_KEY')
secret_key = os.getenv('SECRET_KEY')
region_name = os.getenv('REGION')

ec2_client = boto3.client('ec2', aws_access_key_id=access_key, aws_secret_access_key=secret_key, region_name='eu-central-1')


# def find_server(filter):

#def get_volumes:

#

