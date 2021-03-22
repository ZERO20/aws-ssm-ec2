# aws-ssm-ec2
Run commands to ec2 instances from boto3

Scripts allow `git pull` on a repository within ec2 instances using SSM - AWS

* [ssm_instanceids.py](./ssm_instanceids.py) uses `InstanceIds`
    * For a a limited number of instances, though you can specify up to 50 IDs.

* [ssm_target.py](./ssm_target.py) uses `Target`
    * Accepts tag key-value pairs to identify the instances to send commands to, you can a send command to tens, hundreds, or thousands of instances at once.


**Note: change commands to do other things**