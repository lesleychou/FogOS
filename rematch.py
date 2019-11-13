from crontab import CronTab

# init
cron = CronTab()

# add new cron job

job = cron.new(command='/Users/lesley/Downloads/FogOS/algo2019_Test.py')

# job settings
job.minute.every(1)

cron.write()