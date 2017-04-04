import Queue
from bs4 import BeautifulSoup
import requests
import threading
import time


news_url_q = Queue.Queue()
news_objects_q = Queue.Queue()
image_q = Queue.Queue()

def acquire_news_urls(url):
 archives_page = requests.get(url)
 soup = BeautifulSoup(archives_page.content, 'html.parser')
 for line in soup.find('span',{'class':'pagetext'}):
  entry = line.find_all('a')
  for news in entry:
   href = news.get('href')
   if href not in ["/archive.cms","/archive/year-2017.cms","/archive/year-2017,month-3.cms"] and  href.split('/')[2] == 'politics-and-nation':
    news_url_q.put('http://economictimes.indiatimes.com' + href)


def network_task_thread(news_url_q,news_obj_q):
 while True:
  url = news_q.get()
  news_page = requests.get(url)
  news_obj_q.put(news_page)


def process_news_obj(news_obj_q,img_q):
 while True:
  news_obj = news_obj_q.get()
  soup = BeautifulSoup(archives_page.content, 'html.parser')
  title = soup.title
  by = soup.article.select('.byline')[0]
  try:
   by.script.extract()
  except:
   pass
  finally:
   author = by.text
  try:
   img_path = soup.article.select('.articleImg')[0].img['src']
  except TypeError:
   pass #get the default image from the database. default image for no image obtained from the news webpage


start = time.time()
for i in range(8):
 worker = threading.Thread(target=task_2,args=(all_news_q,))
 worker.setDaemon(True)
 worker.start()

for i in range(8):
 worker = threading.Thread(target=task_3,args=(image_q,))
 worker.setDaemon(True)
 worker.start()


urls = ['http://economictimes.indiatimes.com/archivelist/year-2017,month-3,starttime-42825.cms']



map(task_1,urls)

image_q.join()
all_news_q.join()
end = time.time()

print('total time taken: ' + str(end - start))

