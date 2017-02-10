#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import re
import requests
import requests_cache
from bs4 import BeautifulSoup

import process_url

news_urls = []


def striphtml(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)


def get_news_div_tag(url):
    requests_cache.install_cache()
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    news_div_tag = soup.find_all('div', {'class': 'artText'})
    return str(news_div_tag)


def print_news(news_urls):
    for url in news_urls[4:]:
        news_in_tag = get_news_div_tag(url)
        news = striphtml(news_in_tag)
        news = news[1:len(news)-1]
        print(news.split())
        sys.exit()

def get_news_urls(index_string):
    all_urls_for_month = []
    requests_cache.install_cache()
    page = requests.get(index_string)
    soup = BeautifulSoup(page.content, 'html.parser')
    for line in soup.find_all('td'):
      entry = line.find_all('a')
      for news in entry:
        if news.find_all('b'):
            subject = '# find a way to get the month here'
        else:
            subject = news.contents[0]
        url = 'http://economictimes.indiatimes.com' + news.get('href')
        all_urls_for_month.append(url)
    news_urls.append(all_urls_for_month)


def get_and_process_index_string_for_news_urls():
    index_string_list = process_url.process_index_string()
    for index_string in index_string_list:
        get_news_urls(index_string)


def start():
    get_and_process_index_string_for_news_urls()
    print_news(news_urls[0])


if __name__ == '__main__':
    start()
