from datetime import datetime
from newsparser.constants import CATEGORIES
"""
Session manages persistence operations for ORM-mapped objects.
"""

from newsparser.models import News, User


def create_news(db, news: News):
    """
    function to write a News model object to db
    """
    # create friend instance
    db.add(news)
    db.commit()
    db.refresh(news)

    return news


def list_news(db):
    """
    Return a list of all existing News records
    """
    all_news = db.query(News).all()
    return all_news


def list_news_from_date(db, from_time):
    news_from_time = db.query(News).filter(News.date_time > from_time)
    return news_from_time


def filter_news_by_cat_date(db, from_time, categories):
    filtered_news = db.query(News).filter((News.date_time > from_time)
                                          & (News.category.in_(categories)))

    return filtered_news


def filter_news_by_cat(db, categories):
    return db.query(News).filter(News.category.in_(categories))


def get_last_news_datetime(db):
    last_record = db.query(News).order_by(News.news_id.desc()).first()
    return last_record.date_time


def create_user(db, user: User):
    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def list_all_users(db):
    all_users = db.query(User).all()
    return all_users


def list_users_by_subscription(db, subscription_type, subscription_day, subscription_time):

    users_by_subscription = db.query(User).filter((User.subscription_type == subscription_type)
                                                  & (User.subscription_day == subscription_day)
                                                  & (User.subscription_time == subscription_time)).all()
    return users_by_subscription


def update_user(db, user_id, new_update_time):
    db.query(User).filter(User.user_id == user_id).update({'last_update': new_update_time})
    db.commit()


def generate_mail_body(db, user):
    # Generate paragraph-separated list of link news.

    news = filter_news_by_cat_date(db=db, from_time=user.last_update,
                                   categories=match_categories(user.subscription_category))
    mail_string = ''

    for element in news:
        mail_string += element.title + '\n'
        mail_string += element.url + '\n\n'

    return mail_string


def match_categories(user_category):
    #  Matching user category (coma-separated string) to news category (one of set)

    if user_category in CATEGORIES:  # single word case
        return [user_category]
    else:
        categories_list = user_category.replace(' ', '').split(',')
        if not all(cat in CATEGORIES for cat in categories_list):  # Something wrong with category string
            return None
        else:
            return categories_list

