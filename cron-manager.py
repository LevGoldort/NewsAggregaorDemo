import os
from crontab import CronTab
import pwd


def get_username():
    return pwd.getpwuid(os.getuid())[0]

dir_path = os.path.dirname(os.path.abspath(__file__))

cron = CronTab(user=get_username())
job = cron.new(command=f'source {dir_path}/venv/bin/activate &&'
                       f'python {dir_path}/cron-news-updater.py')

job.minute.every(1)
cron.write()
