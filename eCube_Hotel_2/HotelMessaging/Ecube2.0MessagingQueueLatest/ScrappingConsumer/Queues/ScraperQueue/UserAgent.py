import requests
def GetUserAgent(domain):
    # print ('----------------Hi------------------------UserAgent')
    print('user agent')

    result = requests.post('http://192.168.8.7/site2/api/v1/getUserAgentName',
                           json={"domainName": domain, "comments": "Comments"})

    #result = requests.post('http://192.168.7.128/site2/api/v1/getUserAgentName',
    #                       json={"domainName": domain, "comments": "Comments"})
    if result.status_code == 200:
        userAgent = result.text
    else:
        userAgent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
    print("Recieved response from getuseragentName service",result)
    print ('UserAgent-----------',type(userAgent))
    return userAgent

x = GetUserAgent('business.conrad.it')
print (x)