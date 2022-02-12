import json

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

from newsparser import models
from newsparser import crud
from newsparser.db import engine, db


def startup():

    models.Base.metadata.create_all(bind=engine)  # Bind engine on startup

    # Create basic categories:

    with open('config.json') as f:
        cfg_dict = json.load(f)

    keywords = cfg_dict['categories']

    for category in keywords:

        news_category = models.NewsCategory(
            category_name=category,
            category_keywords=keywords[category]
        )
        crud.create_category(db=db, category=news_category)

    subscriptions = cfg_dict['subscriptions']

    for subscription in subscriptions:

        new_subscription = models.Subscription(
            short_name=subscription,
            long_name=subscriptions[subscription]['long_name'],
            cron_setting=subscriptions[subscription]['cron_setting']
        )
        crud.create_subscription(db, new_subscription)


if __name__ == "__main__":
    pass
