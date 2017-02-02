
import time
import requests
from bs4 import BeautifulSoup

import pythonUrl as pU
import os
count = 0

def write_news_to_file(url, subject):
	try:
		buffer_string = url +' '+ subject + '\n'
		file_handler.write(buffer_string)	
	except UnicodeEncodeError:
		print url,subject
		#modified_string = subject.replace('\u','')
		#buffer_string = url + ' : ' + modified_string + '\n'
		#file_handler.write(buffer_string)	
		pass

def tinyUrl_of(index_string):
	page = requests.get(index_string)
	soup = BeautifulSoup(page.content,'html.parser')
	for line in soup.find_all('td'):
		entry = line.find_all('a')
		for news in entry:
			if news.find_all('b'):
				subject = '# find a way to get the month here'
			else:
		               subject = news.contents[0]

			url = pU.make_tiny('http://economictimes.indiatimes.com'+news.get('href'))
			write_news_to_file(url,subject)
			#print url,subject
			
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
				global count
				month_string = month_base_string + str(month)
				start_time_index_string = start_time_base_string + str(start_time_index)
				index_string = index_base_string + year_string + ',' + month_string + ',' + start_time_index_string + addendum
				tinyUrl_of(index_string)
				count+= 1
				start_time_index += 1


def post_process(file_name):
	post_process_string = 'sh post_process.sh ' + file_name  
	os.system(post_process_string)	

def html_conversion(file_name):
	contents = open(file_name,'r')
	with open('index.html','w') as html_file:
		html_file.write('<table>\n')
		for lines in contents.readlines():
			html_file.write('<tr><td>%s</td></tr>\n' %lines.split())
		
		html_file.write('</table>\n')



if __name__ == '__main__':
	file_name = 'archive_list-'+time.strftime("%S_%M_%H-%d_%m_%Y")+'.txt'
	file_handler = open(file_name,'w',0)
	process_index_string()
	file_handler.close()
	print count
#	post_process(file_name)
#	html_conversion(file_name)

		



