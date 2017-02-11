#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import re
import requests
import requests_cache
import sqlite3
from bs4 import BeautifulSoup

import process_url

database_name = 'news.db'
connection = sqlite3.connect(database_name)
cursor = connection.cursor()
cursor.execute('''CREATE TABLE news (subject text, article text)''') #initialize database


def striphtml(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)


def get_news_div_tag(url):
    requests_cache.install_cache()
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    news_div_tag = soup.find_all('div', {'class': 'artText'})
    return str(news_div_tag)

def get_news(url):
    news_in_tag = get_news_div_tag(url)
    news = striphtml(news_in_tag)
    news = news[1:len(news)-1]  # think of a way to remove this. it consumes memory. debug why you are getting square brackets in the first place.
    return news

def get_news_and_store_in_database(index_string):
    #global connection
    #global cursor
    count = 1
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
        content = get_news(url)
        count += 1
        print(subject,content)
        cursor.execute("INSERT INTO news VALUES (?,?)", (subject,content))
        connection.commit()
        if count > 5:
           connection.close()
            

def get_and_process_index_string_for_news_urls():
    index_string_list = process_url.process_index_string()
    for index_string in index_string_list:
        get_news_and_store_in_database(index_string)


def start():
    get_and_process_index_string_for_news_urls()
       

if __name__ == '__main__':
    start()
