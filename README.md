This script shows simple Continuous Delivery (CD) and Continuous Deployment (CD) approches.

Make sure that you have AWS credentials file, wich you can create mannually

cat ~/.aws/credentials
[ireland]
aws_access_key_id = AKIAIOSFODNN7EXAMPLE                                #DON'T TRY. THESE ARE FAKE
aws_secret_access_key = wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY        #DON'T TRY. THESE ARE FAKE
region = eu-west-1

'''
'''

You are encouraged to set "mashine_name" variable to something meaningfull.
machine_name='Kusnetsov008'

ORDER MATTERS
1. ./create_ec2_ssh_connect.py install_dependences
2. ./create_ec2_ssh_connect.py httpsrv cron
3. ./create_ec2_ssh_connect.py httpsrv

install_dependences - install Python, git, pip
cron - Install cron job on remote Linux mashine
httpsrv - Install http server on remote EC2 instance
