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

sudo $pkg_manager install python3 python35 git -y

sudo $pkg_manager install python-setuptools -y
sudo easy_install pip

sudo $pkg_manager install python-pip3 -y
export PATH=$PATH:/usr/local/bin

curl -O https://bootstrap.pypa.io/get-pip.py
sudo python3 get-pip.py
#pip and pip3 installed

python <(curl https://bootstrap.pypa.io/get-pip.py) --user
pybase=$(python -c 'import site; print site.USER_BASE,')
echo export PATH=\"$pybase/bin:\$PATH\" >> ~/.bash_profile

sudo pip3 install paramiko --user
sudo pip3 install botocore --user
sudo pip3 install boto3 --user


