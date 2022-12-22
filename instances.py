
# Create t2.micro instance for the standalone MYSQL instance
def create_standalone_instance(ec2, securityGroup, subnet_id):
    instance = ec2.create_instances(
        ImageId="ami-0574da719dca65348",
        InstanceType="t2.micro",
        KeyName="vockey",
        UserData=open('standalone_setup.sh').read(),
        SubnetId=subnet_id,
        SecurityGroupIds=[
            securityGroup
        ],
        MaxCount=1,
        MinCount=1,
        TagSpecifications=[
        {
            'ResourceType': 'instance',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': 'MYSQL-Standalone'
                },
            ]
        },
        ]
        )

    return instance


# Create t2.micro instances for the cluster
def create_cluster_instance(ec2, ip_address, securityGroup, userdata, instance_name, subnet_id):
    instance = ec2.create_instances(
        ImageId="ami-0574da719dca65348",
        InstanceType="t2.micro",
        KeyName="vockey",
        UserData=userdata,
        PrivateIpAddress=ip_address,
        SubnetId=subnet_id,
        SecurityGroupIds=[
            securityGroup
        ],
        MaxCount=1,
        MinCount=1,
        TagSpecifications=[
        {
            'ResourceType': 'instance',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': instance_name
                },
            ]
        },
        ]
        )

    return instance


# Create t2.large instance for the proxy
def create_proxy_instance(ec2, ip_address, securityGroup, subnet_id):
    instance = ec2.create_instances(
        ImageId="ami-0574da719dca65348",
        InstanceType="t2.large",
        KeyName="vockey",
        UserData=open('proxy_setup.sh').read(),
        PrivateIpAddress=ip_address,
        SubnetId=subnet_id,
        SecurityGroupIds=[
            securityGroup
        ],
        MaxCount=1,
        MinCount=1,
        TagSpecifications=[
        {
            'ResourceType': 'instance',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': "proxy"
                },
            ]
        },
        ]
        )

    return instance


# This function is defined to terminate the instance.
def terminate_instance(client, instanceId):
    print('terminating instance:')
    print(instanceId)
    client.terminate_instances(InstanceIds=(instanceId))