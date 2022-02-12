import json

from crontab import CronTab
import newsparser.constants as const
import newsparser.crud as crud
from newsparser import models
from newsparser.db import engine, db

# TODO move to main.py, eliminate this
# TODO requirements.txt
# Advanced ptyhton scheduler (Google)
# eliminate if name == main everythere
import logging


logging.basicConfig(level=logging.INFO)


def startup():
    models.Base.metadata.create_all(bind=engine)  # Bind engine on startup

    # Create basic categories:

    with open('config.json') as f:
        keywords = json.load(f)['categories']

    for category in keywords:

        news_category = models.NewsCategory(
            category_name=category,
            category_keywords=keywords[category]
        )

        crud.create_category(db=db, category=news_category)

    # crud.create_category(db=get_db(), category=const.sports)
    # crud.create_category(db=get_db(), category=const.politics)
    # crud.create_category(db=get_db(), category=const.finance)
    # crud.create_category(db=get_db(), category=const.weather)


    #  upsert alchemy

# cron = CronTab(user=const.USERNAME)
# job = cron.new(command=f'source {DIR}/venv/bin/activate && '
#                        f'python {DIR}/cron-news-updater.py')
# job.minute.every(10)

# cron.write()

print(crud.get_categories(db))
