from email import header
import imp
from urllib import request, parse
from urllib.robotparser import RobotFileParser

rp = RobotFileParser()
rp.set_url('https://www.jianshu.com/robot.txt')
rp.read()
print(rp.can_fetch('*', 'http://www.jianshu.com/p/b67554025d7d'))
print(rp.can_fetch('*', 'http://www.jianshu.com/search?q=python&page=1&type=collections'))



# url = 'http://httpbin.org/post'
# header = {
#     'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',  
#     'Host': 'httpbin.org'  
# }

# dict = {'name':'Germey'}
# data = bytes(parse.urlencode(dict), encoding='utf-8')
# req = request.Request(url=url, data=data, headers=header, method='POST')
# response = request.urlopen(req)
# print(response.read().decode('utf-8'))


# response = urllib.request.urlopen('https://github.com/Python3WebSpider/Python3WebSpider')
# # print(response.read().decode('utf-8'))
# # print(type(response))
# print(response.status)
# print(response.getheaders())
# print(response.getheader("Server"))

# try:
#     rp = urllib.request.urlopen('http://httpbin.org/get', timeout=0.1)
# except urllib.error.URLError as e:
#     if isinstance(e.reason, socket.timeout):
#         print('time out')

# request = urllib.request.Request('https://python.org')
# response = urllib.request.urlopen(request)
# print(response.read().decode('utf-8'))
