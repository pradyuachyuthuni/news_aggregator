import Queue
from bs4 import BeautifulSoup
import requests
import threading
import time
from StringIO import StringIO
from PIL import Image
import logging
from datetime import date

news_url_queue = Queue.Queue(maxsize=-1)
news_objects_queue = Queue.Queue(maxsize=-1)
news_url_lagged_queue = Queue.Queue(maxsize=-1)
lagged_objects_queue = Queue.Queue(maxsize=-1)

logging.basicConfig(filename="logger.log",filemode='w',datefmt='%M:%S',level=logging.INFO)
lagged_entries = []
date_url_archives = []



def get_date_url_archives():
  base_date = date(1899,12,30)
  year = 2013
  #for month in [1,2,3,4,5,6,7,8,9,10,11,12]:
  for month in [9,10,11,12]:
    if month in [1,3,5,7,8,10,12]:
     days = 31
    elif month in [4,6,9,11]:
     days = 30
    else:
     days = 28
    for day in range(1,days+1):
     cd = date(year,month,day)
     start_time_number = (cd - base_date).days
     date_url = 'http://economictimes.indiatimes.com/archivelist/year-{},month-{},starttime-{}.cms'.format(year,month,start_time_number)
     date_url_archives.append(date_url)

def acquire_news_urls(url):
 archives_page = requests.get(url)
 soup = BeautifulSoup(archives_page.content,'html.parser')
 content_boxes = soup.body.select('.contentbox5')[1:3]
 soup2 = BeautifulSoup(''.join([str(x) for x in content_boxes]), 'html.parser')
 news_links = soup2.find_all('a')
 for link in news_links:
   href = link.get('href')
   if href.split('/')[2] == 'politics-and-nation':
     entry = 'http://economictimes.indiatimes.com' + href
     news_url_queue.put(entry)
      
def network_task_thread(news_url_q,news_obj_q):
 while True:
  url = news_url_q.get()
  news_page = requests.get(url)
  news_obj_q.put(news_page)
  news_url_q.task_done()

def process_news_object(news_obj_q):
 while True:
  news_obj = news_obj_q.get()
  soup = BeautifulSoup(news_obj.content,'html.parser')
  
  title = soup.title.get_text()
  
  try:
   news_href = str(soup.article.select('.cmtLinks')[0].a['href'])
  except (IndexError,AttributeError) as e:
   pass
  
  try:
   by = soup.article.select('.byline')[0]
   by.script.extract()
  except (IndexError,AttributeError) as e:
   pass
  finally:
   author = str(by.text)
   if 'By' not in author:
    lagged_entries.append(news_href)
   
  try:
   img_path = soup.article.select('.articleImg')[0].img['src']
  except (TypeError,IndexError,AttributeError) as e:
   pass #get the default image from the database. default image for no image obtained from the news webpage
  finally:
   img_path = 'None'
   pass
  
  try:
   content = soup.article.select('.section1')[0].get_text()
  except (TypeError,IndexError,AttributeError) as e:
   pass #get the default image from the database. default image for no image obtained from the news webpage
  finally:
   data = title + '|' + news_href + '|' + author + '|' + img_path +  '|' + content
   logging.info(data)
  
  news_obj_q.task_done()

def download_images(img_q):
  while True:
    img_path,img_name = img_q.get().split(';')
    img_obj = requests.get(img_path)
    i = Image.open(StringIO(img_obj.content))
    try:
     i.save(img_name+'.jpg')
    except IOError:
     i = Image.open(StringIO(img_obj.content)).convert('RGB')
    i.save(img_name+'.jpg')
    img_q.task_done()


for i in range(16):
 worker1 = threading.Thread(target=network_task_thread,args=(news_url_queue,news_objects_queue,))
 worker1.setDaemon(True)
 worker1.start()

for i in range(1):
 worker2 = threading.Thread(target=process_news_object,args=(news_objects_queue,))
 worker2.setDaemon(True)
 worker2.start()

#base_string = 'http://economictimes.indiatimes.com/archivelist/year-2017,month-3,starttime-42'
#addendum = '.cms'
#urls = [base_string + str(i) + addendum for i in range(736,856)]

get_date_url_archives()
print date_url_archives
map(acquire_news_urls,date_url_archives)

news_url_queue.join()
news_objects_queue.join()

for i in range(16):
 worker3 = threading.Thread(target=network_task_thread,args=(news_url_lagged_queue,lagged_objects_queue,))
 worker3.setDaemon(True)
 worker3.start()

for i in range(1):
 worker2 = threading.Thread(target=process_news_object,args=(lagged_objects_queue,))
 worker2.setDaemon(True)
 worker2.start()

logging.info(lagged_entries)
for index,value in enumerate(lagged_entries):
 value = value.replace('/opinions/','/articleshow/')
 news_url_lagged_queue.put('http://economictimes.indiatimes.com' + value)

news_url_lagged_queue.join()
lagged_objects_queue.join()

print('done')

