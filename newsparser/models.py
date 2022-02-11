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
    email = Column(String())
    subscription_type = Column(String())  # Can be ASAP, Daily, Weekly
    subscription_day = Column(String())  # Can be ASAP, Daily, Friday, Sunday
    subscription_time = Column(String())  # Can be ASAP, 10am, 9am, 7pm, 10pm
    last_update = Column(DateTime)  # The time news were sent to user previously
