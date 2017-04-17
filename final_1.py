import Queue
from bs4 import BeautifulSoup
import requests
import threading
import time
from StringIO import StringIO
from PIL import Image

news_url_queue = Queue.Queue()
news_objects_queue = Queue.Queue()
image_queue = Queue.Queue()

def acquire_news_urls(url):
 archives_page = requests.get(url)
 soup = BeautifulSoup(archives_page.content,'html.parser')
 for line in soup.find('span',{'class':'pagetext'}):
   entry = line.find_all('a')
   for news in entry:
     href = news.get('href')
     if href not in ["/archive.cms","/archive/year-2017.cms","/archive/year-2017,month-3.cms"] and  href.split('/')[2] == 'politics-and-nation':
      entry = 'http://economictimes.indiatimes.com' + href
      news_url_queue.put(entry)
      
def network_task_thread(news_url_q,news_obj_q):
 while True:
  url = news_url_q.get()
  news_page = requests.get(url)
  news_obj_q.put(news_page)
  news_url_q.task_done()

def process_news_object(news_obj_q,img_q):
 while True:
  news_obj = news_obj_q.get()
  soup = BeautifulSoup(news_obj.content,'html.parser')
  tilte = soup.title
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
  finally:
   cms_number = soup.article.select('.cmtLinks')[0].a['href'].split('/')[-1].split('.')[0]
   img_q.put(img_path+';'+cms_number)
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


for i in range(4):
 worker1 = threading.Thread(target=network_task_thread,args=(news_url_queue,news_objects_queue,))
 worker1.setDaemon(True)
 worker1.start()

for i in range(1):
 worker2 = threading.Thread(target=process_news_object,args=(news_objects_queue,image_queue,))
 worker2.setDaemon(True)
 worker2.start()

for i in range(8):
 worker3 = threading.Thread(target=download_images,args=(image_queue,))
 worker3.setDaemon(True)
 worker3.start()


urls = ['http://economictimes.indiatimes.com/archivelist/year-2017,month-3,starttime-42824.cms']

start = time.time()

map(acquire_news_urls,urls)

news_url_queue.join()
news_objects_queue.join()
image_queue.join()

end = time.time()

print('total time taken: ' + str(end - start))

