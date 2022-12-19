import time
import boto3
import paramiko
import subprocess
from instances import *
from securityGroup import *


def main():
    
    ec2_client = boto3.client('ec2',
        aws_access_key_id="ASIAQJSMAGZD5GMZYTQH",
        aws_secret_access_key="nlS8ywQoW9gi9Lv3sS/a73PrekpKKjLGw6LTFZ5B",
        aws_session_token="FwoGZXIvYXdzECoaDDdAdzGNl7uD+g7o6SLEAaRQSb18CxuuyfaMORI5tkibOzkgxHRXk8WkklpuyuKq/zB+K2xKZuUxeC9w2M+j4XazVPSHUoDVh+sm78qZmQgECslXZ52ml8M3n15QBOkyV+vJfGxbxDCsH/108t0fE+uUtnblusX+ZokuDcvi0ovObyBu/+VRt5U111ZANH1oGpqiVN4VYydzjR3dZ9WYqQgRf3hgvQu7HL0L1idxbmLFVLbGKzAZShybGCrxGY88MonHOpRbPMnTQQWl+4M3h991yHAoy+r+nAYyLSCek+6XDf4LJqtPYk37qyLeqARzOw9YG21CCR2+v/OrjmHRt6K76d3ppet08w==",
        region_name= 'us-east-1'
        )

    ec2_resource = boto3.resource('ec2',
        aws_access_key_id="ASIAQJSMAGZD5GMZYTQH",
        aws_secret_access_key="nlS8ywQoW9gi9Lv3sS/a73PrekpKKjLGw6LTFZ5B",
        aws_session_token="FwoGZXIvYXdzECoaDDdAdzGNl7uD+g7o6SLEAaRQSb18CxuuyfaMORI5tkibOzkgxHRXk8WkklpuyuKq/zB+K2xKZuUxeC9w2M+j4XazVPSHUoDVh+sm78qZmQgECslXZ52ml8M3n15QBOkyV+vJfGxbxDCsH/108t0fE+uUtnblusX+ZokuDcvi0ovObyBu/+VRt5U111ZANH1oGpqiVN4VYydzjR3dZ9WYqQgRf3hgvQu7HL0L1idxbmLFVLbGKzAZShybGCrxGY88MonHOpRbPMnTQQWl+4M3h991yHAoy+r+nAYyLSCek+6XDf4LJqtPYk37qyLeqARzOw9YG21CCR2+v/OrjmHRt6K76d3ppet08w==",
        region_name= 'us-east-1'
        )
    
    
    #get vpc_id
    vpc_id = ec2_client.describe_vpcs().get('Vpcs', [{}])[0].get('VpcId', '')
     # create security group
    security_group = create_standalone_security_group(ec2_client,"standalone_group",vpc_id)
    
    time.sleep(10)

    # Create EC2 instance
    instance = create_standalone_instance(ec2_resource, security_group['GroupId'])

    print("Waiting for standalone instance to be ok...")
    waiter = ec2_client.get_waiter('instance_status_ok')
    waiter.wait(InstanceIds=[instance[0].id])
    
    # Get public IP
    reservations = ec2_client.describe_instances(InstanceIds=[instance[0].id])['Reservations']
    ip = reservations[0]["Instances"][0].get('PublicIpAddress')
    
    time.sleep(180)
    
    print("STANDALONE BENCHMARK:")
    
    key = paramiko.RSAKey.from_private_key_file("labsuser.pem")
    SSHClient = paramiko.SSHClient()
    SSHClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    SSHClient.connect(ip, username='ubuntu', pkey=key)
    print('Connected to: ' + str(ip))

    commands = [
        "sudo sysbench oltp_read_write --table-size=100000 --mysql-db=sakila --db-driver=mysql --mysql-user=root prepare",
        "sudo sysbench oltp_read_write --table-size=100000 --mysql-db=sakila --db-driver=mysql --mysql-user=root --num-threads=6 --max-time=60 --max-requests=0 run > standaloneBenchmark.txt", 
        "sudo sysbench oltp_read_write --table-size=100000 --mysql-db=sakila --db-driver=mysql --mysql-user=root cleanup"
    ]
    for command in commands:
        # print("Executing "+ command)
        stdin , stdout, stderr = SSHClient.exec_command(command)
        print(stdout.read())
        print(stderr.read())
    
    print("SCP the benchmark results into local folder...")
    subprocess.call(['scp', '-o','StrictHostKeyChecking=no', '-o', 'UserKnownHostsFile=/dev/null', '-i', 'labsuser.pem', "ubuntu@" + str(ip) + ":standaloneBenchmark.txt", '.'])
    
    print("Terminating instance...")
    terminate_instance(ec2_client, [instance[0].id])
    print("Giving 3 min to make sure vpc endpoints from instance are gone before deleting security group...")
    time.sleep(180)
    print("Terminating security group...")
    delete_security_group(ec2_client, security_group['GroupId'])


main()

