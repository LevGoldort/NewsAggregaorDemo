from newsparser import models
from newsparser.db import engine
from newsparser.parse import parse_ynet
from datetime import datetime, timedelta
import newsparser.crud as crud
from newsparser.db import get_db
from newsparser.models import User

# create the database tables on startup or reload
models.Base.metadata.create_all(bind=engine)

now = datetime.now()
delta = timedelta(hours=15)
results = parse_ynet(from_time=now)

for res in results:
    crud.create_news(db=get_db(), news=res)

for element in crud.list_news_from_date(db=get_db(), from_time=now-delta):
    print(element.news_id, element.url, element.date_time, sep='\n')

print(crud.get_last_news_datetime(db=get_db()))

lev = User(name='Lev Goldort',
           email='lev.goldort@gmail.com',
           subscription_type='ASAP',
           subscription_day='ASAP',
           subscription_time='ASAP',
           last_update=datetime.now())

oleg = User(name='Oleg Kropotkin',
            email='oleg.kropot@gmail.com',
            subscription_type='Daily',
            subscription_day='Daily',
            subscription_time='7pm',
            last_update=datetime.now())

# crud.create_user(db=get_db(), user=lev)
# crud.create_user(db=get_db(), user=oleg)

filtered_users = crud.list_users_by_subscription(db=get_db(), subscription_type='Daily',
                                                 subscription_day='Daily',
                                                 subscription_time='7pm')

for user in filtered_users:
    print(user.name)
