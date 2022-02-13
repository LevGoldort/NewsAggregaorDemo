import argparse
import re
import sys
from datetime import datetime

from newsparser.db import db
from newsparser.models import User, Base
from newsparser.db import engine
from newsparser import crud


def check_email(email:str) -> bool:
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if re.fullmatch(regex, email):
        return True
    return False


def generate_subscription_help() -> str:
    subscriptions = crud.get_subscriptions(db)
    result = 'Type number of one of these subscription options: \n'
    for subscription in subscriptions:
        result += f'{subscription.subscription_id} - {subscription.long_name} \n'

    return result


def generate_category_help() -> str:
    categories = crud.get_category_names(db)
    result = 'Choose some of these names and separate with coma. Do not use spaces!'
    for category in categories:
        result += f'{category}, '

    return result


def check_subscriptions_types(subscription_type):
    return True


def check_category(news_category):
    if crud.match_categories(news_category):
        return True
    return False


# Create the parser
my_parser = argparse.ArgumentParser(fromfile_prefix_chars='@')

my_parser.add_argument('name',
                       help='The name of user you want to add, must be one string without spaces')

my_parser.add_argument('email',
                       help='Email for user you want to add, must be valid')

my_parser.add_argument('subscription_type',
                       help=generate_subscription_help())

my_parser.add_argument('news_category',
                       help=generate_category_help())

# Execute parse_args()
args = my_parser.parse_args()

if not check_email(args.email):
    sys.exit('Incorrect email')

if not check_subscriptions_types(args.subscription_type):
    sys.exit('Subscription number is incorrect, please, write number from the list')

if not check_category(args.news_category):
    sys.exit('News category is wrong. Do not use spaces, please!')

user = User(
            name=args.name,
            email=args.email,
            news_categories=args.news_category,
            subscription_id=args.subscription_type,
            news_received=0,
            last_update=datetime.now()
        )
Base.metadata.create_all(bind=engine)
crud.create_user(db=db, user=user)

print('User successfully added to database')
