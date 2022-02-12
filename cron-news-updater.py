from newsparser import models
from newsparser.db import engine
from newsparser.parse import parse_ynet
from datetime import datetime, timedelta
import newsparser.crud as crud
from newsparser.db import get_db
from newsparser.constants import DIR
from newsparser.output import send_mail


def get_initial_news():
    now = datetime.now()
    delta = timedelta(hours=48)
    results = parse_ynet(now - delta)
    print('Initial news loading finished successfully. Loaded news for 48 hours.')
    return results


def update_news():
    models.Base.metadata.create_all(bind=engine)  # Bind engine on startup
    try:
        from_time = crud.get_last_news_datetime(db=get_db())
    except:
        from_time = datetime.now() - timedelta(hours=24)  # If no last news in DB - load news for 24h

    results = parse_ynet(from_time=from_time)
    with open(f'{DIR}/output.txt', 'a') as f:
        f.write(f'From time {from_time} we found {results} results!')

    for res in results:
        crud.create_news(db=get_db(), news=res)

    with open(f'{DIR}/output.txt', 'a') as f:
        f.write('Ran update at {} \n'.format(datetime.now()))

    update_users('ASAP', 'ASAP', 'ASAP')


def update_users(subscription_type, subscription_day, subscription_time):
    """Function selects user by subsctiption type and send them all the news we received from their last update
    and updates last update time for the user to current time"""

    users_to_update = crud.list_users_by_subscription(db=get_db(),
                                                      subscription_type=subscription_type,
                                                      subscription_day=subscription_day,
                                                      subscription_time=subscription_time)
    for user in users_to_update:
        mail_body = crud.generate_mail_body(db=get_db(), user=user)
        send_mail(user.email, mail_body)
        crud.update_user(db=get_db(), user_id=user.user_id, new_update_time=datetime.now())


if __name__ == '__main__':
    update_news()
