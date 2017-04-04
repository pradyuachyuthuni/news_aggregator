import Queue
from bs4 import BeautifulSoup
import requests
import threading
import time
from django.utils.html import strip_tags
from StringIO import StringIO
from PIL import Image
import logging

logging.basicConfig(filename="logger.log",filemode='w',format='%(asctime)s,%(msecs)d %(name)s %(threadName)s %(levelname)s %(message)s',datefmt='%M:%S',level=logging.DEBUG)

all_news_q = Queue.Queue()
image_q = Queue.Queue()

def task_1(url):
 archives_page = requests.get(url)
 #logging the requests.get status_code
 logging.info('N/W request.get : archive page url. status code=%s' %archives_page.status_code)
 soup = BeautifulSoup(archives_page.content, 'html.parser')
 for line in soup.find('span',{'class':'pagetext'}):
  entry = line.find_all('a')
  for news in entry:
   href = news.get('href')
   if href not in ["/archive.cms","/archive/year-2017.cms","/archive/year-2017,month-3.cms"] and  href.split('/')[2] == 'politics-and-nation':
    all_news_q.put('http://economictimes.indiatimes.com' + href) 
    logging.debug('Inserting %s into queue.' % href.split('/')[-1])
 logging.info('Inserted all href(s) into queue.')

def task_2(q):
 while True:
  url = q.get()
  logging.info('Obtained url from all_news_q queue.')
  news_page = requests.get(url)
  logging.info('N/W request.get : news url. status code=%s' %news_page.status_code)
  soup = BeautifulSoup(news_page.content,'html.parser')
  try:
   img = soup.find('article').find('div', {'class':'articleImg'}).find('img')['src']
  except TypeError:
   #log info: image for this news artice is not available.
   img = None
  image_name = url.split('/')[-1].split('.')[0] 
  image_q.put(image_name+';'+img)  
  title = soup.find('article').find('h1', {'class':'title'})
  heading = title.text
  by = soup.find('article').find('div', {'class' : 'byline'})
  if by('script'):
    tmp = by.script.extract() 
  author = by.text.split('|')[0]
  fullText = soup.find('article').find('div', {'class':'Normal'}).text
  textString = strip_tags(fullText)
  length = len(textString.split())
  q.task_done()


def task_3(q):
 while True:
  entry = q.get()
  logging.info('Obtained img src from image_q queue.')
  image_name,url = entry.split(';')
  if url is not None:
   image = requests.get(url)
   i = Image.open(StringIO(image.content))
   try:
    i.save(image_name+'.jpg')
   except IOError:
    i = Image.open(StringIO(image.content)).convert('RGB')
    i.save(image_name+'.jpg')

start = time.time()
for i in range(8):
 worker = threading.Thread(target=task_2,args=(all_news_q,))
 worker.setDaemon(True)
 worker.start()

for i in range(8):
 worker = threading.Thread(target=task_3,args=(image_q,))
 worker.setDaemon(True)
 worker.start()



#urls = ['http://economictimes.indiatimes.com/archivelist/year-2017,month-3,starttime-42825.cms']
urls = ['http://economictimes.indiatimes.com/archivelist/year-2017,month-3,starttime-42817.cms','http://economictimes.indiatimes.com/archivelist/year-2017,month-3,starttime-42818.cms']
#urls = ['http://economictimes.indiatimes.com/archivelist/year-2017,month-3,starttime-42812.cms','http://economictimes.indiatimes.com/archivelist/year-2017,month-3,starttime-42813.cms','http://economictimes.indiatimes.com/archivelist/year-2017,month-3,starttime-42814.cms','http://economictimes.indiatimes.com/archivelist/year-2017,month-3,starttime-42815.cms','http://economictimes.indiatimes.com/archivelist/year-2017,month-3,starttime-42816.cms','http://economictimes.indiatimes.com/archivelist/year-2017,month-3,starttime-42817.cms','http://economictimes.indiatimes.com/archivelist/year-2017,month-3,starttime-42818.cms']

map(task_1,urls)

image_q.join()
all_news_q.join()
end = time.time()

print('total time taken: ' + str(end - start))
