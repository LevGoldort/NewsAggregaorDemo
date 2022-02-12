import newsparser.crud as crud
from newsparser.db import get_db

if __name__ == "__main__":
    for element in crud.list_news(db=get_db()):
        print(element.news_id, element.title, element.url, element.date_time, sep='\n')

    for element in crud.list_all_users(db=get_db()):
        print(element.user_id, element.name, element.subscription_type)
