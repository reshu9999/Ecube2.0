from ops import ProxyHandler, UserRunHandler

domain = 'domain'
request_id = 23061991
userrun_handler = UserRunHandler('OPS', 'NORMAL', request_id)
userrun_handler.set_request_details()
t1, t2 = userrun_handler.get_type(request_id)
# userrun_handler.remove_request_details(request_id)

response = ProxyHandler(domain, request_id).get_proxy
# ProxyHandler.block_proxy(response[1], domain, 'lasun ho gaya')
print(response)

from pdb import set_trace; set_trace()
