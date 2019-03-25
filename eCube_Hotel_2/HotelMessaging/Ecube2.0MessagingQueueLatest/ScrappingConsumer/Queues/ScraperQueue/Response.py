import urllib3
import ssl
import requests

#import sys
from lxml import html


import time

#urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def GetProxy(domain,country):
    print("Get proxy called")
    #result = requests.get(
    #    "http://192.168.7.128/site4/api/v1/getProxy?domain=" + domain + "&country=" + country)

    result = requests.get(
        "http://192.168.8.7/site4/api/v1/getProxy?domain=" + domain + "&country=" + country)
    if result.status_code == 200:
        return result.json()
    else:
        return False

    # result = requests.get(
    #      "http://38.76.27.161/site4/api/v1/getProxy?domain=" + domain + "&country=" + country)



def SaveProxyDetails(domain, proxyserver, proxyport, proxyusername, proxystatus, proxyconutry, proxyregion, proxytype):
    print("The Domain Name is :" + domain)
    #result = requests.get(
    #    "http://192.168.7.128/site4/api/v1/proxy?Domain=" + domain + "&Proxyserver=" + proxyserver + "&ProxyPort=" + proxyport + "&proxyusername=" + proxyusername + "&ProxyStatus=" + proxystatus + "&ProxyCountry=" + proxyconutry + "&proxyRegion=" + proxyregion + "&ProxyType=" + proxytype)

    result = requests.get(
       "http://192.168.8.7/site4/api/v1/proxy?Domain=" + domain + "&Proxyserver=" + proxyserver + "&ProxyPort=" + proxyport + "&proxyusername=" + proxyusername + "&ProxyStatus=" + proxystatus + "&ProxyCountry=" + proxyconutry + "&proxyRegion=" + proxyregion + "&ProxyType=" + proxytype)


def GetUserAgent(domain):


    import  os
    if os.environ.get('http_proxy'):

        print(os.environ.pop('http_proxy'))
        print(os.environ.pop('https_proxy'))
        print(os.environ.pop('ftp_proxy'))
        print(os.environ.pop('socks_proxy'))

    result = requests.post('http://192.168.8.7/site2/api/v1/getUserAgentName',
                           json={"domainName": domain, "comments": "Comments"})
    #result = requests.post('http://192.168.7.128/site2/api/v1/getUserAgentName',json={"domainName": domain, "comments": "Comments"})
    if result.status_code == 200:
        userAgent = result.json()
        print ('userAgent-----------------------','200 status from useragent')
    else:
        userAgent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
        print('userAgent-----------------------', 'Status other than 200')
    # print("Recieved response from getuseragentName service",result)
    return str(userAgent)
