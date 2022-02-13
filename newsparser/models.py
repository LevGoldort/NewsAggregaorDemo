from sqlalchemy import Column, Integer, String, DateTime
from .db import Base


# model/table
class News(Base):
    __tablename__ = "news"

    # fields
    news_id = Column(Integer(), primary_key=True, index=True)  # Make just id
    url = Column(String())
    date_time = Column(DateTime())
    title = Column(String())
    text = Column(String())
    category = Column(String())


class User(Base):
    __tablename__ = "users"

    # fields
    user_id = Column(Integer(), primary_key=True, index=True)  # Make just id
    name = Column(String())
    email = Column(String())
    subscription_id = Column(Integer())
    news_received = Column(Integer())
    news_categories = Column(String())
    last_update = Column(DateTime)  # The time news were sent to user previously


class Subscription(Base):
    __tablename__ = 'subscriptions'

    # fields
    subscription_id = Column(Integer(), primary_key=True, index=True)  # Make just id
    short_name = Column(String(), unique=True)
    long_name = Column(String())
    cron_setting = Column(String())


class NewsCategory(Base):
    __tablename__ = 'categories'

    # fields
    category_id = Column(Integer(), primary_key=True, index=True)  # Make just id
    category_name = Column(String(), unique=True)
    category_keywords = Column(String())
