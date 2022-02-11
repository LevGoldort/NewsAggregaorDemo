from newsparser import models
from newsparser.db import engine
from newsparser.parse import parse_ynet
from datetime import datetime, timedelta
import newsparser.crud as crud
from newsparser.db import get_db


def get_initial_news():
    models.Base.metadata.create_all(bind=engine)
    now = datetime.now()
    delta = timedelta(hours=48)
    results = parse_ynet(now - delta)
    print('Initial news loading finished successfully. Loaded news for 48 hours.')
    return results


def update_news():
    try:
        from_time = crud.get_last_news_datetime(db=get_db())
        results = parse_ynet(from_time=from_time)
    except:
        results = get_initial_news()

    for res in results:
        crud.create_news(db=get_db(), news=res)

    with open('output.txt', 'a') as f:
        f.write('Ran update at {}'.format(datetime.now()))


if __name__ == '__main__':

    update_news()
