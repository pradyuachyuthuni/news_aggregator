from bs4 import BeautifulSoup
import requests
from django.utils.html import strip_tags
from PIL import Image
from StringIO import StringIO
import time
from multiprocessing.dummy import Pool as ThreadPool 
import sys

archive_url = ['http://economictimes.indiatimes.com/archivelist/year-2017,month-3,starttime-42812.cms']
url = []


def get_all_properties(url):
	#html page of url
	htmlPage = requests.get(url)
	soup = BeautifulSoup(htmlPage.content,'html.parser')

	# image
	#img = soup.find('article').find('div', {'class':'articleImg'}).find('img')['src']
	#image = requests.get(img)
	#i = Image.open(StringIO(image.content))
	#image_name = url.split('/')[-1].split('.')[0] + '.jpg'
	#try:
	#	i.save(image_name)
	#except IOError:
	#	i = Image.open(StringIO(image.content)).convert('RGB')
   	#	i.save(image_name)

	# article heading
	#title = soup.find('article').find('h1', {'class':'title'})
	#heading = title.text

	#author, date and time
	#by = soup.find('article').find('div', {'class' : 'byline'})
	#author = by.text.split('|')[0]

	#content length
	#fullText = soup.find('article').find('div', {'class':'Normal'}).text
	#textString = strip_tags(fullText)
	#length = len(textString.split())

	#string_to_print = image_name + " " + author + " " + str(length)
	#print string_to_print

def collect_urls():
	global url
	global archive_url
	for index_string in archive_url:
	  page = requests.get(index_string)
    	  soup = BeautifulSoup(page.content, 'html.parser')
    	  for line in soup.find('span',{'class':'pagetext'}):
      	    entry = line.find_all('a')
      	    for news in entry:
	      st = news.get('href')
	      if st in ["/archive.cms","/archive/year-2017.cms","/archive/year-2017,month-3.cms"]:
	        pass
	      elif st.split('/')[2] == 'politics-and-nation':
	        url.append('http://economictimes.indiatimes.com' + st)

start = time.time()
collect_urls()
print(url)
sys.exit()
pool = ThreadPool(16)
pool.map(get_all_properties,url)
pool.close()
pool.join()
print "Time spent: " + str(time.time() - start)
