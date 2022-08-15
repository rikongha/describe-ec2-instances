# DevOps Test
___
A script to find and return server information and attached EBS volumes.

## Configure
set credentials in the AWS credentials file, and set environment variable 
- `ENVIRONMENT = local` if running locally and 
- `PROFILE = {profilename}` if not using default.

## list.py
run script using `python list.py {name-of-server}` to find a specific server or `python list.py` or `python list.py '*'` to list all. 


## Dependencies
- python3
- boto3
- tabulate
Ensure to have the dependencies above installed, you can run `pip install requirements.txt`.