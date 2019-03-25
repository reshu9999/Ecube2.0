import os
import sys
import json
import time

from queues.executor import ScriptHandler

with open(sys.argv[1], 'r+') as file_obj:
    crawled_data = json.loads(file_obj.read())

parsed_datas = ['No Data from Script Execution']
try:
    error_lines = list()
    for data in crawled_data:
        parsed_data = ScriptHandler(data)._execute_script_function(1)
        # parsed_data = ScriptHandler(data).execute_parse()
        print(parsed_data.keys())
        print(parsed_data['hotel'])
        parsed_datas.append(parsed_data)
        if not parsed_datas:
            error_lines.append('\nNo Data from Script Execution for Input\n%s' % json.dumps(data))
except Exception as e:
    import traceback
    crawled_data = None
    type_, value_, traceback_ = sys.exc_info()
    error_lines = traceback.format_tb(traceback_)

if parsed_datas:
    file_data = parsed_datas
    file_identifier = 'parsed_data'
else:
    file_data = "\n".join(error_lines)
    file_identifier = 'error_data'

from pdb import set_trace; set_trace()
file_distincter = time.time()
with open('%s_%s_%s.json' % (crawled_data['ParserScript'], file_identifier, file_distincter), 'w+') as file_obj:
    print("filename")
    print(os.path.abspath('') + '/' + file_obj.name)
    file_obj.write(json.dumps(file_data))

