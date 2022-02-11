from sqlalchemy.orm import Session

"""
Session manages persistence operations for ORM-mapped objects.
"""

from newsparser.models import News


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

