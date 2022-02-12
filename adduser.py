import argparse
import re
import newsparser.crud as crud
import sys
from newsparser.db import get_db
from newsparser.models import User, Base
from datetime import datetime
from newsparser.db import engine

def check_email(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if re.fullmatch(regex, email):
        return True
    return False


def check_subscriptions_types(subscription_type, subscription_day, subscription_time):
    if subscription_type == 'ASAP':
        if subscription_day == 'ASAP':
            if subscription_time == 'ASAP':
                return True
            else:
                return False
        else:
            return False

    if subscription_type == 'Daily':
        if subscription_day == 'Daily':
            if subscription_time in ['7PM', '10PM']:
                return True
            else:
                return False
        else:
            return False

    if subscription_type == 'Weekly':
        if subscription_day in ['Friday', 'Sunday']:
            if subscription_time in ['10AM', '9AM']:
                return True
            else:
                return False
        return False

    return False


def check_category(news_category):
    if crud.match_categories(news_category):
        return True
    return False


# Create the parser
my_parser = argparse.ArgumentParser(fromfile_prefix_chars='@')

my_parser.add_argument('name',
                       help='The name of user you want to add')

my_parser.add_argument('email',
                       help='Email for user you want to add')

my_parser.add_argument('subscription_type',
                       help='Subscription type, can be ASAP, Daily, Weekly')

my_parser.add_argument('subscription_day',
                       help='Must be ASAP for ASAP, Daily for Daily and Friday or Sunday for Weekly')

my_parser.add_argument('subscription_time',
                       help='Must be ASAP for ASAP, 7PM or 10PM for Daily and 10AM or 9AM for Weekly')

my_parser.add_argument('news_category',
                       help='Coma-separated words from sports, politics, weather, finance')

# Execute parse_args()
args = my_parser.parse_args()

if not check_email(args.email):
    sys.exit('Email is in incorrect format')

if not check_subscriptions_types(args.subscription_type, args.subscription_day, args.subscription_time):
    sys.exit('Subscription types are not correct. Can be ASAP ASAP ASAP, '
             'Daily Daily ["7PM", "10PM"], Weekly ["Friday", "Sunday"], ["9AM", "10AM"]')

if not check_category(args.news_category):
    sys.exit('News category is wrong. Pick some from sports, finance, weather, politics and separate with coma!')
user = User(
            name=args.name,
            email=args.email,
            subscription_category=args.news_category,
            subscription_type=args.subscription_type,
            subscription_day=args.subscription_day,
            subscription_time=args.subscription_time,
            last_update=datetime.now()
        )
Base.metadata.create_all(bind=engine)
crud.create_user(db=get_db(), user=user)
print('User successfully added to database')
