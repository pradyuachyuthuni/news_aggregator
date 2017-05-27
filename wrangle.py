import os
import sys
from django.utils.html import strip_tags

class NewsObject:
  def __init__(self, title=None, author=None, date_and_time=None, article_link=None, image_path=None, content=None):
    self.title = title
    self.author = author
    self.date_and_time = date_and_time
    self.article_link = article_link
    self.image_path = image_path
    self.content = content

  def write_news_capsule_to_file(self):
    fd.write(strip_tags(str(self.__dict__)))
    fd.write('\n')

def create_raw_data_file(log_file):
    input_file_copy = 'copy_' + log_file
    raw_data_file = 'test.log'
    os.system('cp {} {}'.format(log_file,input_file_copy))
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
     if length is 5:
      title,article_link,date_and_time,image_path,content = obj_contents_list
      author = "Inhouse"
     elif length is 6:
      title,article_link,author,date_and_time,image_path,content = obj_contents_list
     elif length > 6:
      title,article_link,author,date_and_time,image_path = obj_contents_list[0:5]
      content = obj_contents_list[5:]
     else:
      print "improper news object found"
     news_object = NewsObject(title,author,date_and_time,article_link,image_path,content)
     news_object.write_news_capsule_to_file()

if __name__ == '__main__':
   args = sys.argv
   if len(args) == 1:
     sys.exit()
   else:
     log_file = str(args[1]) 
     fd = open('{}_news_database.txt'.format(log_file.split('.')[0]),'w',0)
     raw_data_file = create_raw_data_file(log_file)
     news_list = cleanup_unwanted_data(raw_data_file)
     instantiate_news_objects(news_list)
    
