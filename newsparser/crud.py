from sqlalchemy.orm import Session
from sqlalchemy import and_

"""
Session manages persistence operations for ORM-mapped objects.
"""

from newsparser.models import News, User


def create_news(db: Session, news: News):
    """
    function to write a News model object to db
    """
    # create friend instance
    db.add(news)
    db.commit()
    db.refresh(news)

    return news


def list_news(db: Session):
    """
    Return a list of all existing News records
    """
    all_news = db.query(News).all()
    return all_news


def list_news_from_date(db: Session, from_time):
    news_from_time = db.query(News).filter(News.date_time > from_time)
    return news_from_time


def get_last_news_datetime(db: Session):
    last_record = db.query(News).order_by(News.news_id.desc()).first()
    return last_record.date_time


def create_user(db: Session, user: User):
    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def list_all_users(db: Session):
    all_users = db.query(User).all()
    return all_users


def list_users_by_subscription(db: Session, subscription_type, subscription_day, subscription_time):
    users_by_subscription = db.query(User).filter((User.subscription_type == subscription_type)
                                                  & (User.subscription_day == subscription_day)
                                                  & (User.subscription_time == subscription_time)).all()
    return users_by_subscription
