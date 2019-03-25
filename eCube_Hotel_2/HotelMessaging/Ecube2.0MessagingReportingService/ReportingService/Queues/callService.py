import requests
def GetProxy(domain, country):
    result = requests.get(
        "http://192.168.7.128/site4/api/v1/getProxy?Domain=" + domain + "&country=" + country)
    return result.text

x = GetProxy('business.conrad.it','Italy')
print (x)