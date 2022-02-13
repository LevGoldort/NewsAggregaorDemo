import json

from sqlalchemy import exc
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

import jobs
from newsparser import models
from newsparser import crud
from newsparser.db import engine, db


def startup():
    """
    Function to initialize DB and to put there basic news_subscriptions and basic news categories. No basic users added.
    :return: None
    """
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
        crud.create_category(db=db, category=news_category)  # Load to DB

    subscriptions_ = cfg['subscriptions']

    for subscription in subscriptions_:

        new_subscription = models.Subscription(
            short_name=subscription,
            long_name=subscriptions_[subscription]['long_name'],
            cron_setting=subscriptions_[subscription]['cron_setting']
        )
        crud.create_subscription(db, new_subscription)  # Load to DB


if __name__ == "__main__":

    try:
        startup()  # If DB is already created, calling startup will raise exception
    except exc.IntegrityError:
        db.rollback()  # In case we need just rerun jobs

    with open('config.json') as f:
        cfg_dict = json.load(f)

    # Crontab setting for news updater:
    news_update_setting = f'*/{cfg_dict["news_update_frequency"]} * * * *'

    scheduler = BlockingScheduler()

    # Job to update the news:
    scheduler.add_job(jobs.update_news,
                      CronTrigger.from_crontab(news_update_setting),
                      kwargs={
                          'ynet_url': cfg_dict['ynet_url'],
                          'sky_url': cfg_dict['sky_url']
                      }
                      )

    # Jobs to send mails to subscribers:
    subscriptions = crud.get_subscriptions(db)
    for sub in subscriptions:
        scheduler.add_job(jobs.update_users,
                          CronTrigger.from_crontab(sub.cron_setting),
                          kwargs={'subscription_id': sub.subscription_id})

    scheduler.start()
