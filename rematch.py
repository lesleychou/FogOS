from crontab import CronTab

# init
cron = CronTab(user=True)

# add new cron job

job = cron.new(command='/Users/lesley/Downloads/FogOS/algo2019_interface.py')

# job settings
job.minute.every(0.5)

cron.write()
