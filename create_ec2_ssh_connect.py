#!/usr/bin/env python3

'''
Install requirements

Install python3 manually for this script to start working.
sudo yum -y install python35 python3 git

sudo yum -y install git

curl -O https://bootstrap.pypa.io/get-pip.py
sudo python3 get-pip.py
#pip and pip3 installed

pip3 install paramiko boto3 --user

'''


import os
from botocore.exceptions import ClientError
import subprocess
import sys
import time

def run_bash_command(command):
    ## call date command ##
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    
    ## Talk with date command i.e. read data from stdout and stderr. Store this info in tuple ##
    ## Interact with process: Send data to stdin. Read data from stdout and stderr, until end-of-file is reached.  ##
    ## Wait for process to terminate. The optional input argument should be a string to be sent to the child process, ##
    ## or None, if no data should be sent to the child.
    (output, err) = p.communicate()
    
    ## Wait for date to terminate. Get return returncode ##
    p_status = p.wait()
    print ("Command output : ", output)
    print ("Command exit status/return code : ", p_status)
    return output



print(run_bash_command("sudo yum -y install git"))

#pip and pip3 install
run_bash_command("curl -O https://bootstrap.pypa.io/get-pip.py")
run_bash_command("sudo python3 get-pip.py")
#pip and pip3 installed

run_bash_command("pip3 install paramiko boto3 --user")



import boto3
import botocore
import paramiko


s = boto3.Session(profile_name='ireland')
ec2 = s.resource('ec2')
ec2_client = s.client('ec2')

#ec2_client = boto3.resource('ec2', region_name="eu-west-1")

machine_name='kusnetsov006'

# Check to see if specified keypair already exists.
# If we get an InvalidKeyPair.NotFound error back from EC2,
# it means that it doesn't exist and we need to create it.
try:
    my_key_name=machine_name
    response = ec2_client.describe_key_pairs(
    KeyNames=[
        my_key_name,
    ],
)
except ClientError as e:
    if e.response['Error']['Code'] == 'InvalidKeyPair.NotFound':
        print ('Creating keypair: %s' % my_key_name)
        # Create an SSH key to use when logging into instances.
        outfile = open(my_key_name + '.pem','w')
        key_pair = ec2.create_key_pair(KeyName=my_key_name)
        # AWS will store the public key but the private key is
        # generated and returned and needs to be stored locally.
        # The save method will also chmod the file to protect
        # your private key.
        KeyPairOut = str(key_pair.key_material)
        outfile.write(KeyPairOut)
        outfile.close()
        os.chmod(my_key_name + '.pem', 0o600)
    else:
        print ('Keypair: %s already exists' % my_key_name)
        raise

def list_instances_by_tag_value(tagkey, tagvalue):
    # When passed a tag key, tag value this will return a list of InstanceIds that were found.

    #ec2client = boto3.client('ec2')

    response = ec2_client.describe_instances(
        Filters=[
            {
                'Name': 'tag:'+tagkey,
                'Values': [tagvalue]
            }
        ]
    )
    instancelist = []
    for reservation in (response["Reservations"]):
        for instance in reservation["Instances"]:
            instancelist.append(instance["InstanceId"])
    return instancelist

#Check if EC2 instance exists
InstanceId=list_instances_by_tag_value('Name', machine_name)
#print(InstanceId)

#Accessing Values in List
#print ("InstanceId: ", InstanceId[0])

create_new_EC2=True

if create_new_EC2:
    if len(InstanceId) == 0:
        print ("Creating new EC2 instance...")
        instances = ec2.create_instances(
        ImageId='ami-047bb4163c506cd98', 
        MinCount=1, 
        MaxCount=1,
        KeyName=my_key_name,
        InstanceType="t2.micro"
        )
        print ("EC2 instance created.")
        instance_id = instances[0].instance_id
        instance = instances[0]
        my_create_volume=True
        my_ssh_connect_section=True
        ###Give name to EC2 instance 
        ec2.create_tags(
        Resources=[instance_id], Tags=[{'Key':'Name', 'Value': machine_name}]
        )
    else:
        print ("EC2 instance exists, InstanceId = ", InstanceId[0])
        instance_id = InstanceId[0]
        #To get instance without creating new instance
        instance = ec2.Instance(instance_id)
        my_create_volume=False
        my_ssh_connect_section=True



#Check if EC2 instance exists
InstanceId=list_instances_by_tag_value('Name', machine_name)
#print(InstanceId)
instance_id = InstanceId[0]
#To get instance without creating new instance
instance = ec2.Instance(instance_id)

# Wait for the instance to enter the running state
instance.wait_until_running()



###Create security group if does not exist.
try:
    grp_name=machine_name    
    mysg = ec2.create_security_group(GroupName=grp_name,Description='Kusnetsovs_Group')
    mysg.authorize_ingress(IpProtocol="tcp",CidrIp="0.0.0.0/0",FromPort=80,ToPort=80)
    mysg.authorize_ingress(IpProtocol="tcp",CidrIp="0.0.0.0/0",FromPort=22,ToPort=22)
    print('Security Group Created %s' % (mysg.id)) 
    ###Attach security group to ec2 instance
    instance_grp = ec2.Instance(instance_id)
    instance_grp.modify_attribute(Groups=[mysg.id])
except ClientError as e:
    if e.response['Error']['Code'] == 'InvalidGroup.Duplicate':
        print ('Group %s exists. We will use it. ' % grp_name)
    

if my_create_volume:
    ###Create volume of magnetic(standart) type 
    volume_response = ec2_client.create_volume(
    Size=1,
    AvailabilityZone='eu-west-1c',
    VolumeType='standard',
    )
    volume_id = volume_response["VolumeId"]
    waiter = ec2_client.get_waiter('volume_available')
    waiter.wait(VolumeIds=[volume_id])
    #print (volume)
    #print(volume_id)

    waiter = ec2_client.get_waiter('instance_running')
    waiter.wait(InstanceIds=[instance_id])

    try:
        ###Attach volume to ec2 instance
        #volume = ec2.Volume('id')
        volume = ec2.Volume(volume_id)
        volume_attach = volume.attach_to_instance(
        InstanceId=instance_id,
        Device='/dev/sds')
        waiter = ec2_client.get_waiter('volume_in_use')
        #print(volume_attach)
        waiter.wait(VolumeIds=[volume_id])
    except ClientError as e:
        if e.response['Error']['Code'] == 'IncorrectState':
            print ('Group %s exists. We will use it. ' % grp_name)


# Reload the instance attributes
instance.load()
print(instance.public_dns_name)



#time.sleep(120) # delays for 1 minute

key_file=str(machine_name + '.pem')

if my_ssh_connect_section:
    
    try:
        key = paramiko.RSAKey.from_private_key_file(key_file)
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    except Exception as e:
            print (e)

    


    def my_ssh_command_bg(mycommand):
        client.connect(hostname=str(instance.public_dns_name), username="ec2-user", pkey=key)
        transport = client.get_transport()
        channel = transport.open_session()
        channel.exec_command(mycommand)


    def my_ssh_command(mycommand):
        # Connect/ssh to an instance
        # Here 'Amazon Linux' is user name and 'instance_ip' is public IP of EC2
        client.connect(hostname=str(instance.public_dns_name), username="ec2-user", pkey=key)
        # Execute a command(cmd) after connecting/ssh to an instance
        stdin, stdout, stderr = client.exec_command(mycommand)
        stdin.flush()
        result = stderr.read()
        if len(result)  > 0:
            print("hit error \n" + str(result))
        data = stdout.read()
        print(data)
        client.close()
        #break
        
        

    try:    
        my_ssh_command('sudo mkfs -t ext4 /dev/sds')
    except Exception as e:
            print (e)    
     
    try:        
        my_ssh_command('sudo mkdir /data -p')
    except Exception as e:
            print (e)
    try:
        my_ssh_command('sudo mount /dev/sds /data')
    except Exception as e:
            print (e)
    try:
        my_ssh_command('df -h')
    except Exception as e:
            print (e)


    try:
        my_ssh_command('sudo yum install git -y')
    except Exception as e:
            print (e)

    try:
        my_ssh_command('cd /data && sudo git clone https://github.com/eu21/test.git')
    except Exception as e:
            print (e)

    

    print ("***")
    next_command='cd /data/test && sudo git pull origin master'
    print (next_command)
    print ("start of output")
    try:
        my_ssh_command(next_command)
    except Exception as e:
            print (e)
            
    print ("finish of output")
    print ("***")        
  

    next_command='sudo yum install python35 python3 -y'
    print (next_command)
    try:
        my_ssh_command(next_command)
    except Exception as e:
            print (e)
    print ("***")
        
    if len(sys.argv) > 1:
        if sys.argv[1]=='httpsrv':   
            
            print ("***")
            next_command='sudo kill $(pgrep -f \'python3 /data/test/httpsrv.py\')'
            #next_command='sudo pkill -f httpsrv.py'
            print (next_command)
            print ("BEGIN of output")
            try:
                my_ssh_command_bg(next_command)
            except Exception as e:
                    print (e)
            print ("END of output")
            print ("***")         
                    
            print ("***")
            next_command='sudo python3 /data/test/httpsrv.py > /dev/null 2>&1 &'
            print (next_command)
            print ("BEGIN of output")
            try:
                my_ssh_command_bg(next_command)
            except Exception as e:
                    print (e)
            print ("END of output")
            print ("***")         



    if len(sys.argv) > 2:
        if sys.argv[2]=='cron':
            print ("***")
            next_command='sudo service crond start && sudo chmod +x /data/test/restart_if_repo_changed.py && /bin/bash /data/test/set_cron_task.sh'
            print (next_command)
            print ("BEGIN of output")
            try:
                my_ssh_command(next_command)
            except Exception as e:
                    print (e)
                    
            print ("END of output")
            print ("***") 

print ('httpsrv started. URL to our site http://%s/' % str(instance.public_dns_name))
print ('SSH on port 22 using command:')            
print ('ssh -i %s ec2-user@%s' % (key_file, str(instance.public_dns_name)))

