import requests

x = requests.get('https://www.baidu.com/')
print(x.status_code)

print(x.reason)

print(x.json())