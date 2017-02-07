import sys
import re
import requests
from bs4 import BeautifulSoup

def striphtml(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)

def get_news_div_tag(url):
	response = requests.get(url)
	soup = BeautifulSoup(response.text, 'html.parser')
	news_div_tag = soup.find_all("div", {"class" : "artText" })
	return str(news_div_tag)

def print_news(url):
	news_in_tag = get_news_div_tag(url)
	news = striphtml(news_in_tag)
	print(news)

if __name__ == '__main__':
	url = sys.argv[1]
	print_news(url)

