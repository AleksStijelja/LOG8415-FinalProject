
# Create t2.micro instance for the standalone MYSQL instance
def create_standalone_instance(ec2, securityGroup):
    print(securityGroup)
    instance = ec2.create_instances(
        ImageId="ami-0574da719dca65348",
        InstanceType="t2.micro",
        KeyName="vockey",
        UserData=open('standalone_setup.sh').read(),
        Placement={
            'AvailabilityZone': 'us-east-1a',
        },
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


# This function is defined to terminate the instance.
def terminate_instance(client, instanceId):
    print('terminating instance:')
    print(instanceId)
    client.terminate_instances(InstanceIds=(instanceId))