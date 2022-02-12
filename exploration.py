import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

# Read DB to dataFrame
con = sqlite3.connect('newsparser.db')
df = pd.read_sql_query("SELECT * from news", con, index_col='news_id')

df['category'] = pd.Categorical(df['category'])
print(df['category'].dtypes)

# most popular categories
ax = df['category'].value_counts().plot(kind='bar',
                                        title='Popularity of categories',
                                        ylabel='Number of news',
                                        xlabel='Category')

plt.show()

