#!/bin/bash


declare -A osInfo;
osInfo[/etc/redhat-release]=yum
osInfo[/etc/arch-release]=pacman
osInfo[/etc/gentoo-release]=emerge
osInfo[/etc/SuSE-release]=zypp
osInfo[/etc/debian_version]=apt-get

for f in ${!osInfo[@]}
do
    if [[ -f $f ]];then
        pkg_manager=${osInfo[$f]}
    fi
done

#echo $pkg_manager

sudo $pkg_manager -y install python3 python35 git

sudo $pkg_manager -y install python-setuptools
sudo easy_install pip

curl -O https://bootstrap.pypa.io/get-pip.py
sudo python3 get-pip.py
#pip and pip3 installed

sudo pip3 install paramiko --user
sudo pip3 install botocore --user
sudo pip3 install boto3 --user

sudo pip install paramiko --user
sudo pip install botocore --user
sudo pip install boto3 --user



