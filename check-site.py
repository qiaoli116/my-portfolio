import boto3
import requests

def stop_ec2_instance(instance_id):
    ec2_client = boto3.client('ec2')
    try:
        ec2_client.stop_instances(InstanceIds=[instance_id])
        print(f"Instance {instance_id} is stopping.")
    except Exception as e:
        print(f"Error stopping instance {instance_id}: {e}")


# Assuming your AWS credentials are configured properly
ec2_client = boto3.client('ec2')

# Describe all instances
response = ec2_client.describe_instances()

ec2_list = []

# Loop through reservations and instances to get public IP addresses
for reservation in response['Reservations']:
    for instance in reservation['Instances']:
        if 'PublicIpAddress' in instance:
            print(f"Instance ID: {instance['InstanceId']}, Public IP: {instance['PublicIpAddress']}")
            ec2 = {
                "InstanceId": instance['InstanceId'],
                "PublicIpAddress": instance['PublicIpAddress']
            }
            ec2_list.append(ec2)

# Print the list of EC2 instances
print(ec2_list)

# for each ec2 instance, check if the site is up using url http://ip/phpMyAdmin
for ec2 in ec2_list:
    url = f"http://{ec2['PublicIpAddress']}/phpMyAdmin"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print(f"{url} up!")
        else:
            print(f"{url} down!")
            stop_ec2_instance(ec2['InstanceId'])
    except requests.ConnectionError:
        print(f"{url} down!")
        stop_ec2_instance(ec2['InstanceId'])
    