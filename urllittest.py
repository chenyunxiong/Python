from ast import keyword
import urllib.request

def requestUrl():
    try:
        url = urllib.request.urlopen("https://github.com/chenjiandongx/51job-spider/blob/master/job_spider.py/")
        print(url.read())
    except urllib.error.HTTPError as e:
        print("connect error")

def headerUrl():
    url = "https://www.runoob.com/?s="
    keyword = 'Python 教程'
    key_code = urllib.request.quote(keyword)
    url_all = url + key_code
    header = {
    'User-Agent':'Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }   #头部信息
    request = urllib.request.Request(url_all, headers=header)
    reponse = urllib.request.urlopen()
# requestUrl()
