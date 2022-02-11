from newsparser import models
from newsparser.db import engine
from newsparser.parse import parse_ynet
from datetime import datetime, timedelta
import newsparser.crud as crud
from newsparser.db import get_db

#create the database tables on app startup or reload
models.Base.metadata.create_all(bind=engine)

now = datetime.now()
delta = timedelta(hours=3)
# results = parse_ynet(now - delta)
# for res in results:
#     crud.create_news(db=get_db(), news=res)

for element in crud.list_news_from_date(db=get_db(), from_time=now-delta):
    print(element.news_id, element.url, element.date_time, sep='\n')
