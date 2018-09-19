#!/usr/bin/env python3
import boto3
s = boto3.Session(profile_name='ireland')
ec2 = s.resource('ec2')
instance = ec2.create_instances(
    ImageId='ami-047bb4163c506cd98',
    MinCount=1,
    MaxCount=1,
    InstanceType='t2.micro')


ec2.create_tags('i-0d9dc74b6aed8af8d', ("Name" = 'Eugene_Kusnetsov'))
