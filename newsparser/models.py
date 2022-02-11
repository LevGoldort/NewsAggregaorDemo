from sqlalchemy import Column, Integer, String, Date, DateTime
from .db import Base


# model/table
class News(Base):
    __tablename__ = "news"

    # fields
    news_id = Column(Integer(), primary_key=True, index=True)
    url = Column(String())
    date_time = Column(DateTime())
    title = Column(String())
    text = Column(String())
    author = Column(String())
    category = Column(String())


class User(Base):
    __tablename__ = "users"

    # fields
    user_id = Column(Integer(), primary_key=True, index=True)
    name = Column(String())
    subscription_type = Column(String())
    subscription_date = Column(String())
    subscription_time = Column(String())
    last_news_id = Column(Integer())
