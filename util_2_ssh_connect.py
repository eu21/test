#!/usr/bin/env python3
import boto3
import botocore
import paramiko

key = paramiko.RSAKey.from_private_key_file('/media/Vera_media_flash16gb_8GB/1SUPPORT/OpsWorks/Test1/Kusnetsov05.pem')
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

def my_ssh_command_bg(mycommand):
    client.connect(hostname='ec2-34-245-10-48.eu-west-1.compute.amazonaws.com', username="ec2-user", pkey=key)
    transport = client.get_transport()
    channel = transport.open_session()
    channel.exec_command(mycommand)


def my_ssh_command(mycommand):
    # Connect/ssh to an instance
    # Here 'Amazon Linux' is user name and 'instance_ip' is public IP of EC2
    client.connect(hostname='ec2-34-245-10-48.eu-west-1.compute.amazonaws.com', username="ec2-user", pkey=key)
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
    
'''    
try:    
    my_ssh_command('sudo mkfs -t ext4 /dev/sds')
except Exception as e:
        print (e)
try:        
    my_ssh_command('sudo mkdir /data')
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

'''

print ("***")
next_command='cd /data/test && sudo git pull origin master'
print (next_command)
print ("BEGIN of output")
try:
    my_ssh_command(next_command)
except Exception as e:
        print (e)
        
print ("END of output")
print ("***")        


'''
try:
    my_ssh_command('cd /data/test && ls')
except Exception as e:
        print (e)
'''



'''
try:
    my_ssh_command('sudo yum update')
except Exception as e:
        print (e)
'''

'''
next_command='yum install python35 -y'
print ("***")
print (next_command)
print ("***")
try:
    my_ssh_command(next_command)
except Exception as e:
        print (e)
'''


        
print ("***")
next_command='sudo python3 /data/test/httpsrv.py /dev/null 2>&1 &'
print (next_command)
print ("BEGIN of output")
try:
    my_ssh_command_bg(next_command)
except Exception as e:
        print (e)
        
print ("END of output")
print ("***")         