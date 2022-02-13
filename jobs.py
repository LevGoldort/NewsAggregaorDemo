from newsparser.parse import parse_ynet, parse_sky
from datetime import datetime
import newsparser.crud as crud
from newsparser.db import db
from newsparser.output import send_mail


def update_news(ynet_url: str, sky_url: str):
    """Function to parse news and send them to db"""
    from_time = crud.get_last_news_datetime(db=db)

    results_ynet = parse_ynet(from_time=from_time, url=ynet_url)
    results_sky = parse_sky(from_time=from_time, url=sky_url)
    results = sorted(results_ynet + results_sky, key=lambda x: x.date_time, reverse=False)
    for res in results:
        crud.create_news(db=db, news=res)


def update_users(subscription_id: int):
    """Function selects user by subscription type and send them all the news we received from their last update
    and updates last update time for the user to current time"""

    users_to_update = crud.list_users_by_subscription(db=db, subscription_id=subscription_id)

    for user in users_to_update:

        news_to_send, mail_body = crud.generate_mail_body(db=db, user=user)

        if news_to_send == 0:  # No news found
            continue

        send_mail(user.email, mail_body)

        # If sending successful - update user:
        crud.update_user(db=db, user_id=user.user_id,
                         new_update_time=datetime.now(),
                         new_news_received=user.news_received + news_to_send)
