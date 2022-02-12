from crontab import CronTab
from newsparser.constants import DIR, USERNAME

cron = CronTab(user=USERNAME)
# job = cron.new(command=f'source {DIR}/venv/bin/activate && '
#                        f'python {DIR}/cron-news-updater.py')
# job.minute.every(10)
# cron.write()

for job in cron:
    print(job)