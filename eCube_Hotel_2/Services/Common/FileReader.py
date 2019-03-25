# from lxml import etree
class FileReader():
    def GetUrls(self,file):
        f = open(file, 'r')
        # urls = f.readlines()
        urls = f.read().split(',')
        return (urls)

    def GetUserAgents(self,file):
        f = open(file, 'r')
        usragnts = f.read().split(',')
        return (usragnts)

    def GetProxies(self,file):
        f = open(file, 'r')
        proxies = f.read().split(',')
        return (proxies)

    def GetUrlsXML(self,file):
        from xml.dom import minidom
        xmldoc = minidom.parse(file)
        itemlist = xmldoc.getElementsByTagName('url')
        urls=[]
        for list in itemlist:
            loc = list.getElementsByTagName("loc")[0]
            # print(loc.firstChild.data)
            urls.append(loc.firstChild.data)
        return urls