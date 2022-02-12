from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger


def job_function():
    print('Hu!')


if __name__ == "__main__":
    sch = BlockingScheduler()
    sch.add_job(job_function, trigger=CronTrigger.from_crontab('* * * * *'))
    sch.start()