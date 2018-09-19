#write out current crontab
crontab -l > /data/test/mycron
#echo new cron into cron file
echo "1 * * * * python3 \data\test\restart_if_repo_changed.py" >> /data/test/mycron
#install new cron file
crontab /data/test/mycron

