# -*- coding: utf-8 -*-

import time

import boto3

ec2_resource = boto3.resource('ec2')
ec2_client = boto3.client('ec2')
ssm_client = boto3.client('ssm')

# Configuration
repo_path = 'repo_path' # repository path on the instance
tag_name = 'tag:enviroment' # replace <enviroment> with tag name
tag_value = 'test' # replace with tag name


def instances_find(name, value):
    """Finds instance id's based on tags.
    Args:
        name (str): tag name
        value (str): tag value

    Returns:
        list: Returns a list of instances found.
    """

    list_instances = []
    # filter based on tags
    filters =[
        {
        'Name': name,
        'Values': [
            value,
            ]
        },
    ]
    instances = ec2_resource.instances.filter(Filters=filters)
    for instance in instances:
        list_instances.append(instance.id)
    return list_instances


def check_command_status(instance_id, command_id):
    """Checks the status of a command on an instance
    """
    try:
        time.sleep(2)
        result = ssm_client.get_command_invocation(
            CommandId=command_id,
            InstanceId=instance_id,
        )
        print(f"{instance_id}: {result['Status']}")
    except ssm_client.exceptions.InvocationDoesNotExist:
        print(f"{instance_id}: Failed")


def run_commands_instance(instance_list):
    '''
        Perform actions on a list of ec2 instances
    '''

    commands = [
        'echo "hello world" > /home/ec2-user/hello.txt', # demo
        f'cd {repo_path}',
        'sudo git pull'
        # do stuff
    ]

    response = ssm_client.send_command(
        InstanceIds=instance_list,
        DocumentName='AWS-RunShellScript',
        Parameters= {'commands':commands},
    )
    command_id = response['Command']['CommandId']
    for instance_id in instance_list:
        check_command_status(instance_id, command_id)


# Find instances
ec2_list = instances_find(tag_name, tag_value)
print(f'Instances found: {ec2_list}')

# Run Command
run_commands = run_commands_instance(ec2_list)