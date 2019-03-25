import sys
import json
import requests
argv = sys.argv[1]
resp = requests.post('http://192.168.8.20/mail/api/v1/send_email/', data=argv)
print(resp)
