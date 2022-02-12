from newsparser import models
from newsparser.db import engine
from newsparser.parse import parse_ynet, parse_sky
from datetime import datetime, timedelta
import newsparser.crud as crud
from newsparser.db import db
from newsparser.output import send_mail


def update_news():
    """Function to parse news and send them to db"""

    models.Base.metadata.create_all(bind=engine)  # Bind engine on startup

    from_time = crud.get_last_news_datetime(db=get_db())

    results_ynet = parse_ynet(from_time=from_time)
    results_sky = parse_sky(from_time=from_time)
    results = sorted(results_ynet + results_sky, key=lambda x: x.date_time, reverse=False)

    for res in results:
        crud.create_news(db=db, news=res)
        print(res.date_time)

    update_users('ASAP', 'ASAP', 'ASAP')  #  Second job


def update_users(subscription_type, subscription_day, subscription_time):
    """Function selects user by subsctiption type and send them all the news we received from their last update
    and updates last update time for the user to current time"""

    users_to_update = crud.list_users_by_subscription(db=db,
                                                      subscription_type=subscription_type,
                                                      subscription_day=subscription_day,
                                                      subscription_time=subscription_time)

    for user in users_to_update:

        mail_body = crud.generate_mail_body(db=db, user=user)
        if not mail_body:
            continue
        send_mail(user.email, mail_body)
        crud.update_user(db=db, user_id=user.user_id, new_update_time=datetime.now())


if __name__ == '__main__':
    update_news()
