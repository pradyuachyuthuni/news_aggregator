index_string_list = []

def process_index_string():
  index_base_string = 'http://economictimes.indiatimes.com/archivelist/'
  year_base_string = 'year-'
  month_base_string = 'month-'
  start_time_base_string = 'starttime-'
  addendum = '.cms'

  start_time_index = 41640

  for year in (range(2014,2015)):
    year_string = year_base_string + str(year)
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
        index_string_list.append(index_string) 
        start_time_index += 1
  return index_string_list

if __name__ == '__main__':
	string_list = process_index_string()
	print(string_list)
	print(len(string_list))
