import os
from crontab import CronTab
from newsparser.models import DIR, USERNAME
import pwd


dir_path = os.path.dirname(os.path.abspath(__file__))

cron = CronTab(user=USERNAME())
# job = cron.new(command=f'source {dir_path}/venv/bin/activate && '
#                        f'python {dir_path}/cron-news-updater.py')
#
# job.minute.every(1)
# cron.write()

for job in cron:
    print(job)