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
    
    ec2_client = boto3.client('ec2',
        aws_access_key_id="ASIAQJSMAGZDRYRKWN76",
        aws_secret_access_key="G2fBywh/h3QJbPQtQCdYAqN85FHilxLVN9bRblNv",
        aws_session_token="FwoGZXIvYXdzEIb//////////wEaDGi54Fao1dIxwgo7fCLEAeRrjzjFcxRDvnAUdDu6SycN4TqwDCqzHiZUbv3k/CnHiaHu7LLYUKD1rJErGgvq5+g8EZxhr2UbK9KTbm6/4k05p8PxuOlu7V2wM9f/BvlhiY4NUn3SUZ2P32uCxWWzqzGDK625zZwIJSU0O9dnlj2SsP2mtJ8FVt7FdhaqOryaw8ajuO09ZBtJLYghyAgjQ8tavc5sTcO12Gixmw0quhRw98T3NAd6CCH06Y9fuAmxH0v5TMcr6YcZgJhiQweJGeeYbIEopPaSnQYyLb9QRJFLKRBhDRLFj8LeD2/gD8MyQi5ePlSJBRk/x2Us+KcuikAlLnmbFturfw==",
        region_name= 'us-east-1'
        )

    ec2_resource = boto3.resource('ec2',
            aws_access_key_id="ASIAQJSMAGZDRYRKWN76",
            aws_secret_access_key="G2fBywh/h3QJbPQtQCdYAqN85FHilxLVN9bRblNv",
            aws_session_token="FwoGZXIvYXdzEIb//////////wEaDGi54Fao1dIxwgo7fCLEAeRrjzjFcxRDvnAUdDu6SycN4TqwDCqzHiZUbv3k/CnHiaHu7LLYUKD1rJErGgvq5+g8EZxhr2UbK9KTbm6/4k05p8PxuOlu7V2wM9f/BvlhiY4NUn3SUZ2P32uCxWWzqzGDK625zZwIJSU0O9dnlj2SsP2mtJ8FVt7FdhaqOryaw8ajuO09ZBtJLYghyAgjQ8tavc5sTcO12Gixmw0quhRw98T3NAd6CCH06Y9fuAmxH0v5TMcr6YcZgJhiQweJGeeYbIEopPaSnQYyLb9QRJFLKRBhDRLFj8LeD2/gD8MyQi5ePlSJBRk/x2Us+KcuikAlLnmbFturfw==",
            region_name= 'us-east-1'
            )
    
    
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