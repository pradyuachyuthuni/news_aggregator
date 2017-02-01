
import time
import requests
from bs4 import BeautifulSoup

import pythonUrl as pU


def write_news_to_file(url, subject):
	file_name = 'archive_list-'+time.strftime("%S_%M_%H-%d_%m_%Y")+'.txt'
	file_handler = open(file_name,'w',0)
	file_handler.write(url,subject)	

def tinyUrl_of(index_string):
	print(index_string)
	page = requests.get(index_string)
	soup = BeautifulSoup(page.content,'html.parser')
	for line in soup.find_all('td'):
		entry = line.find_all('a')
		for news in entry:
			#print pU.make_tiny('http://economictimes.indiatimes.com'+news.get('href')), news.contents[0]
			write_news_to_file(pU.make_tiny('http://economictimes.indiatimes.com'+news.get('href')), news.contents[0])
			
def process_index_string():
	index_base_string = 'http://economictimes.indiatimes.com/archivelist/'
	year_base_string = 'year-'
	month_base_string = 'month-'
	start_time_base_string = 'starttime-'
	addendum = '.cms'
	
	start_time_index = 41640
	
	#for year in (2014,2015,2016):
	for year in (range(2014,2015)):
		year_string = year_base_string + str(year)
		#for month in (1,2,3,4,5,6,7,8,9,10,11,12):
		for month in (range(1,2)):
			if (month == 1 or month == 3 or month == 5 or month == 7 or month == 8 or month == 10 or month == 12):
 				count_upper_limit = 1
			elif (month == 4 or month == 6 or month == 9 or month == 11):
 				count_upper_limit = 30
			elif (year == 2004 or year == 2008 or year == 2012 or year == 2016):
 				count_upper_limit = 29
			else:
				count_upper_limit = 28
			
			for i in range(1,count_upper_limit + 1):	
				month_string = month_base_string + str(month)
				start_time_index_string = start_time_base_string + str(start_time_index)
				index_string = index_base_string + year_string + ',' + month_string + ',' + start_time_index_string + addendum
				tinyUrl_of(index_string)
				start_time_index += 1

if __name__ == '__main__':
	process_index_string()
