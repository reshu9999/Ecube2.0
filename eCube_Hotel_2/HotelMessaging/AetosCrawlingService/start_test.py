import os
import sys
import json
import copy
import time

from queues.core import ScriptDataMaker
from queues.executor import ScriptHandler

if len(sys.argv) > 1:
    first_arg = sys.argv[1]
else:
    first_arg = 'Travel'

if isinstance(first_arg, dict):
    crawl_input = first_arg
else:
    try:
        crawl_input = json.loads(first_arg)
    except json.JSONDecodeError as e:
        print(str(e))
        crawl_input = ScriptDataMaker(first_arg).script_data

print(json.dumps(crawl_input))
try:
    crawled_data = ScriptHandler(crawl_input).execute_crawl(False)
    if not crawled_data:
        error_lines = ['No Data from Script Execution for Input\n%s' % json.dumps(crawl_input)]
except Exception as e:
    import traceback
    crawled_data = None
    type_, value_, traceback_ = sys.exc_info()
    error_lines = traceback.format_tb(traceback_)

if crawled_data:
    crawled_hotel_master = copy.deepcopy(crawled_data)
    hotels = crawled_hotel_master.pop('hotels')
    crawled_hotels = list()
    for h in hotels:
        crawled_hotel = copy.deepcopy(crawled_hotel_master)
        crawled_hotel['hotel'] = h
        crawled_hotels.append(crawled_hotel)
    file_data = crawled_hotels
    file_identifier = 'crawled_data'
else:
    file_data = "\n".join(error_lines)
    file_identifier = 'error_data'


from pdb import set_trace; set_trace()
file_distincter = time.time()
with open('%s_%s_%s.json' % (crawl_input['ScraperScript'], file_identifier, file_distincter), 'w+') as file_obj:
    print("filename")
    print(os.path.abspath('') + '/' + file_obj.name)
    file_obj.write(json.dumps(file_data))

