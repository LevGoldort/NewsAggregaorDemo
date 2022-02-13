import json
from datetime import datetime, timedelta

from sqlalchemy import exc
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

import jobs
from newsparser import models
from newsparser import crud
from newsparser.db import engine, db


def startup():

    models.Base.metadata.create_all(bind=engine)  # Bind engine on startup

    # Create basic categories:

    with open('config.json') as file:
        cfg = json.load(file)

    keywords = cfg['categories']

    for category in keywords:

        news_category = models.NewsCategory(
            category_name=category,
            category_keywords=keywords[category]
        )
        crud.create_category(db=db, category=news_category)

    subscriptions = cfg['subscriptions']

    for subscription in subscriptions:

        new_subscription = models.Subscription(
            short_name=subscription,
            long_name=subscriptions[subscription]['long_name'],
            cron_setting=subscriptions[subscription]['cron_setting']
        )
        crud.create_subscription(db, new_subscription)

    user = models.User(
            name='Lev',
            email='lev.goldort@gmail.com',
            news_categories='sports,politics,finance,weather',
            subscription_id=1,
            news_received=0,
            last_update=datetime.now() - timedelta(hours=15)
        )

    crud.create_user(db, user)


if __name__ == "__main__":

    try:
        startup()  # If DB is already created, calling startup will raise exception
    except exc.IntegrityError:
        db.rollback()  # In case we need just rerun jobs

    with open('config.json') as f:
        cfg_dict = json.load(f)

    news_update_setting = f'*/{cfg_dict["news_update_frequency"]} * * * *'  # Crontab setting

    scheduler = BlockingScheduler()

    # Job to update the news:
    scheduler.add_job(jobs.update_news,
                      CronTrigger.from_crontab(news_update_setting),
                      kwargs={
                          'ynet_url': cfg_dict['ynet_url'],
                          'sky_url': cfg_dict['sky_url']
                      }
                      )

    # Jobs to send mails:
    subscriptions = crud.get_subscriptions(db)
    for sub in subscriptions:
        scheduler.add_job(jobs.update_users,
                          CronTrigger.from_crontab(sub.cron_setting),
                          kwargs={'subscription_id': sub.subscription_id})

    scheduler.start()
