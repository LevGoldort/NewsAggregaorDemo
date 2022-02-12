from datetime import datetime, timedelta

from sqlalchemy.orm import Session
from newsparser.models import News, User, Subscription, NewsCategory

import newsparser.db


def create_news(db: Session, news: News) -> News:
    """
    function to write a News model object to db
    """
    # create friend instance
    db.add(news)
    db.commit()
    db.refresh(news)

    return news


def list_news(db: Session) -> list:
    """
    Return a list of all existing News records
    """
    all_news = db.query(News).all()
    return all_news


def list_news_from_date(db: Session, from_time: datetime) -> list:
    """
    Return a list of all existing News records older than given from_time
    """
    news_from_time = db.query(News).filter(News.date_time > from_time)

    return news_from_time


def filter_news_by_cat_date(db: Session, from_time: datetime, categories: list) -> list:
    """
    Return a list of all existing News records older than given from_time and matching the given categories
    """
    filtered_news = db.query(News).filter((News.date_time > from_time)
                                          & (News.category.in_(categories)))

    return filtered_news


def get_last_news_datetime(db: Session) -> datetime:
    """
    Get the latest added news datetime when it was written to website
    """
    last_record = db.query(News).order_by(News.news_id.desc()).first()  # if empty = return datetime - timedelta
    return last_record.date_time or datetime.now() - timedelta(hours=24)


def create_user(db: Session, user: User) -> User:
    """
    Add User object to db
    """
    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def list_all_users(db: Session) -> list:
    all_users = db.query(User).all()
    return all_users


def list_users_by_subscription(db: Session, subscription_id):
    """
    """

    users_by_subscription = db.query(User).filter((User.subscription_id == subscription_id)).all()
    return users_by_subscription


def update_user(db: Session, user_id: int, new_update_time: datetime, new_news_received: int):
    """
    Update user last_update
    """
    db.query(User).filter(User.user_id == user_id).update({'last_update': new_update_time,
                                                           'news_received': new_news_received})
    db.commit()


def generate_mail_body(db: Session, user: User) -> str:
    """
    Generating a mail body with unread news for user.
    Title + Link to the news
    """

    news = filter_news_by_cat_date(db=db, from_time=user.last_update,
                                   categories=match_categories(user.subscription_category))
    mail_string: str = ''

    for element in news:
        mail_string += element.title + '\n'
        mail_string += element.url + '\n\n'

    return mail_string


def match_categories(user_category: str):
    """Matching user category (coma-separated string) to news category (one of set)"""
    categories = get_category_names(db=newsparser.db.db)
    if user_category in categories:  # single word case
        return [user_category]
    else:
        categories_list = user_category.replace(' ', '').split(',')
        if not all(cat in categories for cat in categories_list):  # Something wrong with category string
            return None
        else:
            return categories_list


def create_category(db: Session, category: NewsCategory) -> NewsCategory:

    db.add(category)
    db.commit()
    db.refresh(category)

    return category


def create_subscription(db: Session, subscription: Subscription) -> Subscription:

    db.add(subscription)
    db.commit()
    db.refresh(subscription)

    return subscription


def get_category_names(db: Session) -> list:
    categories = [element[0] for element in db.query(NewsCategory.category_name).all()]
    return categories


def get_categories(db: Session) -> list:

    categories = db.query(NewsCategory).all()
    return categories
