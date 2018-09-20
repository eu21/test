#write out current crontab file
crontab -l > mycron
#echo new cron into cron file
#echo "1 * * * * root python3 /data/test/restart_if_repo_changed.py" > mycron
echo "* * * * * /usr/bin/python3 /data/test/restart_if_repo_changed.py" >> mycron
#install new cron file
crontab mycron

