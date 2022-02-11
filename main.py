from newsparser import models
from newsparser.db import engine
from newsparser.parse import parse_ynet
from datetime import datetime, timedelta
import newsparser.crud as crud
from newsparser.db import get_db
from newsparser.models import User
from newsparser.output import send_mail


def filter_news(user):
    pass


# create the database tables on startup or reload

models.Base.metadata.create_all(bind=engine)

for element in crud.list_news(db=get_db()):
    print(element.news_id, element.url, element.date_time, element.category, sep='\n')

send_mail('lev.goldort@gmail.com', 'here will be message linksjjjjjjjjj 211')


#
# lev = User(name='Lev Goldort',
#            email='lev.goldort@gmail.com',
#            subscription_type='ASAP',
#            subscription_day='ASAP',
#            subscription_time='ASAP',
#            last_update=datetime.now())
#
# oleg = User(name='Oleg Kropotkin',
#             email='oleg.kropot@gmail.com',
#             subscription_type='Daily',
#             subscription_day='Daily',
#             subscription_time='7pm',
#             last_update=datetime.now())

# crud.create_user(db=get_db(), user=lev)
# crud.create_user(db=get_db(), user=oleg)
#
# filtered_users = crud.list_users_by_subscription(db=get_db(), subscription_type='Daily',
#                                                  subscription_day='Daily',
#                                                  subscription_time='7pm')
#
# for user in filtered_users:
#     print(user.user_id, user.name, user.last_update)
#
# crud.update_user(db=get_db(), user_id=2, new_update_time=datetime.now())
#
# filtered_users = crud.list_users_by_subscription(db=get_db(), subscription_type='Daily',
#                                                  subscription_day='Daily',
#                                                  subscription_time='7pm')
#
# for user in filtered_users:
#     print(user.user_id, user.name, user.last_update)
#
# send_mail('glevgo@gmail.com', 'Hey, fellows!')
