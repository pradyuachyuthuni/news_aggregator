import os
import time
import re

class NewsObject:
  def __init__(self, title=None, author=None, date_and_time=None, article_link=None, image_path=None, content=None):
    self.title = title
    self.author = author
    self.date_and_time = date_and_time
    self.article_link = article_link
    self.image_path = image_path
    self.content = content

  def print_news_capsule(self):
    print self.title 
    print self.author
    print self.date_and_time
    print self.article_link
    print self.image_path 
    print self.content
    print "------------------------- END OF OBJECT -------------------------"

def create_raw_data_file():
    input_file = 'april.log'
    input_file_copy = 'copy_' + input_file
    raw_data_file = 'test.log'
    os.system('cp {} {}'.format(input_file,input_file_copy))
    os.system("tr -d '\n' < {} > {}".format(input_file_copy,raw_data_file))
    return raw_data_file

def cleanup_unwanted_data(raw_data_file):
    unwanted_string = 'INFO:requests.packages.urllib3.connectionpool:Starting new HTTP connection (1): economictimes.indiatimes.com'
    delimiter = 'INFO:root:'
    with open(raw_data_file) as f:
     for line in f:
      single_raw_news_string = ''.join(str(line))
    news_list = single_raw_news_string.replace(unwanted_string,'').split(delimiter)[1:]
    return news_list
   
def instantiate_news_objects(news_list):
    for news_item in news_list:
     object_internal_separator = '|'
     obj_contents_list = news_item.split(object_internal_separator)
     length = len(obj_contents_list)
     #if length == 5:
     #  regex = r"""[a-zA-Z]+ [0-3][0-9], \d+, [0-9][0-9].[0-9][0-9] [A|P]M IST"""
     #  if re.match(regex,obj_contents_list[1]):
     #    article_link,date_and_time,title,image_path,content = obj_contents_list
     #    author = None
     if length is not 6:
       for x in obj_contents_list[4:6]:
        print x
       time.sleep(5)
       print "_--------------------------------------------------------------_"
       #article_link,author,date_and_time,title,image_path,content = obj_contents_list
     #news_object = NewsObject(title,author,date_and_time,article_link,image_path,content)
     #news_object.print_news_capsule()

if __name__ == '__main__':
    raw_data_file = create_raw_data_file()
    news_list = cleanup_unwanted_data(raw_data_file)
    instantiate_news_objects(news_list)
