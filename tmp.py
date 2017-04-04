import requests
from bs4 import BeautifulSoup
from django.utils.html import strip_tags
import processURL


#urls = ['http://economictimes.indiatimes.com/nri/visa-and-immigration/us-clears-air-around-h-1b-visa-with-policy-memorandum-computer-programmers-wont-be-eligible/articleshow/57999318.cms','http://economictimes.indiatimes.com/markets/stocks/news/in-a-first-since-1991-fdi-flow-takes-care-of-cad/articleshow/58000640.cms','http://economictimes.indiatimes.com/tech/ites/infosys-ceo-vishal-sikka-defends-coo-pravin-raos-pay-says-move-crucial-to-retain-talent/articleshow/57998877.cms','http://economictimes.indiatimes.com/news/politics-and-nation/donald-trump-may-get-involved-in-india-pakistan-peace-process-nikki-haley/articleshow/58001616.cms']


urls = []

def task_1(url):
 archives_page = requests.get(url)
 soup = BeautifulSoup(archives_page.content, 'html.parser')
 for line in soup.find('span',{'class':'pagetext'}):
  entry = line.find_all('a')
  for news in entry:
   href = news.get('href')
   if href not in ["/archive.cms","/archive/year-2017.cms","/archive/year-2017,month-3.cms"] and  href.split('/')[2] == 'politics-and-nation':
    urls.append('http://economictimes.indiatimes.com' + href)


def printstuff(url):
 news = requests.get(url)
 soup = BeautifulSoup(news.content,'html.parser')
 print(soup.title.text)
 author = soup.article.select('.byline')[0]
 try:
  author.script.extract()
 except:
  pass
 finally:
  print(author.text)
 #print(strip_tags(soup.select(".artText")[0].select(".Normal")[0]))
 #try:
 # print(soup.article.select('.articleImg')[0].img['src'])
 #except TypeError:
 # pass
 print('-----------------------') 


task_1('http://economictimes.indiatimes.com/archivelist/year-2017,month-4,starttime-42828.cms')
for i in range(len(urls)):
 printstuff(urls[i])
