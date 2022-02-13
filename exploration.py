import re
import sqlite3

import pandas as pd
import matplotlib.pyplot as plt


def define_domain(url: str) -> str:  # Get domain name from link

    exp = r'\bhttps?://(?:www\.|ww2\.)?((?:[\w-]+\.){1,}\w+)\b'
    r = re.compile(exp, re.M)
    domain = r.findall(url)[0]

    return domain


# Read DB to dataFrame
con = sqlite3.connect('newsparser.db')
df = pd.read_sql_query("SELECT * from news", con, index_col='news_id')


df['category'] = pd.Categorical(df['category'])

# show most popular categories
ax = df['category'].value_counts().plot(kind='bar',
                                        title='Popularity of categories',
                                        ylabel='Number of news',
                                        xlabel='Category',
                                        rot=0)

plt.savefig('figures/MostPopularNewsCat.png')


# Get domain from URL and make it category
df['domain'] = df['url'].apply(define_domain)
df['domain'] = pd.Categorical(df['domain'])

# Show domains and number of news from them
df['domain'].value_counts().plot(kind='bar',
                                 title='Popularity of domains',
                                 ylabel='Number of news',
                                 rot=0)

plt.savefig('figures/SitesByNews.png')


# Show most popular categories by domain
grouped = df.groupby('domain')
grouped['category'].value_counts().unstack().plot(
    kind='bar',
    rot=0
)

plt.savefig('figures/CategoryByDomain.png')


# get hour of news published from datetime:
df['date_time'] = pd.to_datetime(df['date_time'])
df['hour'] = df['date_time'].dt.hour

grouped = df['hour'].sort_values().value_counts().plot(kind='bar',
                                                       xlabel='hour',
                                                       ylabel='Number of news',
                                                       title='Most busy hour')

plt.savefig('figures/MostBusyHour.png')
