import subprocess
import sys
import time
import boto3
from instances import *
from securityGroup import *


def main():
    
    if len(sys.argv) < 2:
        print('ERROR! Make sure the command has the (172.31.16.0/20) subnet, like this => python3 proxy_setup.py "subnet-XXXXXXXXXXXXXXXXX"')
        exit()
        
    subnet_id = str(sys.argv[1])
    
    ec2_client = boto3.client("ec2", region_name="us-east-1")

    ec2_resource = boto3.resource("ec2", region_name="us-east-1")
    
    
    #get vpc_id
    vpc_id = ec2_client.describe_vpcs().get('Vpcs', [{}])[0].get('VpcId', '')
     # create security group
    security_group = create_proxy_security_group(ec2_client,"proxy_group",vpc_id)
    
    time.sleep(10)

    # Create EC2 instance
    instance = create_proxy_instance(ec2_resource, "172.31.17.5", security_group['GroupId'], subnet_id)

    print("Waiting for the proxy instance to be ok...")
    waiter = ec2_client.get_waiter('instance_status_ok')
    waiter.wait(InstanceIds=[instance[0].id])
    
    time.sleep(180)
    
    print("Ready!")

    # Get public IP
    reservations = ec2_client.describe_instances(InstanceIds=[instance[0].id])['Reservations']
    ip = reservations[0]["Instances"][0].get('PublicIpAddress')

    print("SCP the labsuser.pem to the proxy...")
    subprocess.call(['scp', '-o','StrictHostKeyChecking=no', '-o', 'UserKnownHostsFile=/dev/null', '-i', 'labsuser.pem', 'labsuser.pem',"ubuntu@" + str(ip) + ":labsuser.pem"])
    
    destroy = False
    while destroy == False:
        answer = input("- Enter 'terminate' to terminate the proxy instance and security group: ")
        if answer == "terminate":
            print("Terminating proxy instance...")
            terminate_instance(ec2_client, [instance[0].id])
            print("Giving 3 min to make sure vpc endpoints from the instance are gone before deleting security group...")
            time.sleep(180)
            print("Terminating security group...")
            delete_security_group(ec2_client, security_group['GroupId'])
            destroy = True
        else:
            continue

main()