from newsparser import models
from newsparser.db import engine
from newsparser.parse import parse_ynet
from datetime import datetime, timedelta
import newsparser.crud as crud
from newsparser.db import get_db
from newsparser.models import User
from newsparser.output import send_mail
from newsparser.constants import CATEGORIES

models.Base.metadata.create_all(bind=engine)

def filter_news(user):
    pass

# create the database tables on startup or reload
#
# models.Base.metadata.create_all(bind=engine)
#

print(crud.get_last_news_datetime(db=get_db()))

for element in crud.list_news(db=get_db()):
    print(element.news_id, element.title, element.url, element.date_time, element.category, sep='\n')
#
#
# for element in crud.list_all_users(db = get_db()):
#     print(element.user_id, element.name, element.subscription_category, element.last_update, sep='\n')

# send_mail('lev.goldort@gmail.com', 'here will be message linksjjjjjjjjj 211')

#
#
lev = User(name='Lev Goldort The Second',
           email='lev.goldort@gmail.com',
           subscription_type='ASAP',
           subscription_day='ASAP',
           subscription_time='ASAP',
           subscription_category='finance, sports, weather, politics',
           last_update=datetime.now())

# oleg = User(name='Oleg Kropotkin',
#             email='oleg.kropot@gmail.com',
#             subscription_type='Daily',
#             subscription_day='Daily',
#             subscription_time='7pm',
#             subscription_category='sports, weather',
#             last_update=datetime.now())
#
crud.update_user(db=get_db(),user_id=3, new_update_time=datetime.now()-timedelta(hours=5))
# # crud.create_user(db=get_db(), user=oleg)
#
#
for user in crud.list_all_users(db=get_db()):
    print(user.user_id, user.name, user.last_update, user.subscription_category)
    print(crud.generate_mail_body(db=get_db(), user=user))

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