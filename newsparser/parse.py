import json
import random
from datetime import datetime

import requests
from bs4 import BeautifulSoup

from newsparser.models import News
from newsparser import crud
from newsparser.db import db


def get_ynet_article_text(url: str) -> str:
    """
    Get news text for DB and categorization
    :param url:
    :return:
    """
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    article = soup.find('script', type='application/ld+json')
    article_dict = json.loads(article.text)

    return article_dict['articleBody']


def get_sky_article_text(url: str) -> str:
    """
    Get news text for DB and categorization
    :param url:
    :return:
    """

    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    article = soup.find('script', type='application/ld+json')
    article_dict = json.loads(article.text)

    if article_dict['@type'] != 'NewsArticle':
        return ''

    return article_dict['articleBody']


def get_sky_article_time(url: str) -> str:
    """
    Sky website has time parametr only on the news page, therefore this function scraps it.
    :param url:
    :return:
    """

    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    article = soup.find('script', type='application/ld+json')
    article_dict = json.loads(article.text)

    if article_dict['@type'] != 'NewsArticle':
        return ''

    if 'dateCreated' in article_dict.keys():
        return article_dict['dateCreated']

    return article_dict['datePublished']


def categorize_article(text: str) -> str:
    """
    Checking text for the keywords and return category string
    :param text: news text
    :return: category
    """

    found_categories = []

    categories = crud.get_categories(db=db)
    cat_list = []

    for category in categories:
        keywords = category.category_keywords.split(',')
        if any(keyword in text for keyword in keywords):
            found_categories.append(category.category_name)
        cat_list.append(category.category_name)

    if not found_categories:
        return random.choice(cat_list)
    else:
        return random.choice(found_categories)


def parse_ynet(url: str, from_time: datetime) -> list:
    """
    Parses news from url to the list of News class. Takes only the news appeared after from_time.
    :param url:
    :param from_time:
    :return:
    """

    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    all_news = soup.find_all('div', class_='slotView')
    result = []

    for news in all_news:

        # Getting news publication time
        date_element = news.find('span', class_='dateView')
        date_time_string = date_element.text.replace(' ', '')
        news_datetime = datetime.strptime(date_time_string, '%H:%M,%m.%d.%y')

        if news_datetime <= from_time:  # No need to parse outdated news
            continue

        title_element = news.find('div', class_='slotTitle')
        title = title_element.text

        link = news.find('a')
        link_url = link['href']

        # Getting article text from the link and categorizing it
        text = get_ynet_article_text(link_url)
        category = categorize_article(text)

        # Creating News object and appending results:
        news_object = News(
            url=link_url,
            date_time=news_datetime,
            title=title,
            text=text,
            category=category
        )
        result.append(news_object)

    return result


def fix_sky_link(url: str) -> str:
    """
    Some sky links are missing domain
    :param url:
    :return:
    """
    if url.find('news.sky.com') == -1:
        return 'https://news.sky.com/'+url
    return url


def parse_sky(url: str, from_time: datetime) -> list:
    """
    Parses news from url to the list of News class. Takes only the news appeared after from_time.

    :param url:
    :param from_time:
    :return:
    """

    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    all_news = soup.find_all('h3', class_='sdc-site-tile__headline')
    result = []

    for news in all_news:

        link = news.find('a')
        link_url = fix_sky_link(link['href'])

        date_time_string = get_sky_article_time(link_url)

        if not date_time_string:
            continue

        news_datetime = datetime.strptime(date_time_string, '%Y-%m-%dT%H:%M:%S')

        if news_datetime <= from_time:  # No need to parse outdated news
            continue

        text = get_sky_article_text(link_url)
        if not text:  # Not parsing live-blogs and non-articles
            continue

        title_element = news.find('span', class_='sdc-site-tile__headline-text')
        title = title_element.text

        category = categorize_article(text)

        news_object = News(
            url=link_url,
            date_time=news_datetime,
            title=title,
            text=text,
            category=category
        )
        result.append(news_object)

    return result
