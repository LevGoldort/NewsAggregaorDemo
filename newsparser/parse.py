import requests
import json
import random
from bs4 import BeautifulSoup
from datetime import datetime
from newsparser.models import News

YNET_URL = 'https://www.ynetnews.com/category/3089'

SPORTS_KEYWORDS = frozenset(['football', 'basketball', 'ski', 'sport', 'olympics', 'athletics', 'tournament'])
POLITICS_KEYWORDS = frozenset(['president', 'prime minister', 'law', 'U.N', 'NATO', 'government',
                               'democrats', 'republicans', 'minister', 'vote', 'politician', 'political party'])
FINANCE_KEYWORDS = frozenset(['dollar', 'stocks', 'shekel', 'bitcoin', 'company', 'sp500', 'nasdaq'])
WEATHER_KEYWORDS = frozenset(['rain', 'snow', 'sunny', 'earthquake', 'clouds', 'storm', 'flood'])
CATEGORIES = frozenset(['sports', 'politics', 'finance', 'weather'])


def get_ynet_article_text(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    article = soup.find('script', type='application/ld+json')
    article_dict = json.loads(article.text)

    return article_dict['articleBody']


def categorize_article(text):
    # Checking text for the keywords and return category string
    found_categories = []

    if any(keyword in text for keyword in SPORTS_KEYWORDS):
        found_categories.append('sports')
    if any(keyword in text for keyword in POLITICS_KEYWORDS):
        found_categories.append('politics')
    if any(keyword in text for keyword in FINANCE_KEYWORDS):
        found_categories.append('finance')
    if any(keyword in text for keyword in WEATHER_KEYWORDS):
        found_categories.append('weather')

    if not found_categories:
        return random.sample(CATEGORIES, 1)[0]

    elif len(found_categories) == 1:  # only one category found
        return found_categories[0]

    else:
        return random.sample(found_categories, 1)[0]


def parse_ynet(from_time):
    # Parses news from YNET_URL to the list of News class. Takes only the news appeared after from_time.

    page = requests.get(YNET_URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    all_news = soup.find_all('div', class_='slotView')
    result = []

    for news in all_news:

        # Getting news publication time
        date_element = news.find('span', class_='dateView')
        date_time_string = date_element.text.replace(' ', '')
        news_datetime = datetime.strptime(date_time_string, '%H:%M,%m.%d.%y')

        if news_datetime < from_time:  # No need to parse outdated news
            continue

        # Getting author, title and link
        author_element = news.find('div', class_='moreDetails')
        author = author_element.find('span', class_='author').text

        title_element = news.find('div', class_='slotTitle')
        title = title_element.text

        link = news.find('a')
        link_url = link['href']

        # Getting article text from the link and categorizing it
        text = get_ynet_article_text(link_url)
        category = categorize_article(text)

        # Creating News object and appending to results:
        news_object = News(
            url=link_url,
            date_time=news_datetime,
            title=title,
            text=text,
            author=author,
            category=category
        )
        result.append(news_object)

    return reversed(result)  # Result reversed to be from earlier to latest datetime


if __name__ == '__main__':
    pass
