import requests     # 发送请求 第三方模块
import re           # 内置模块 无需安装


# x = 1
url = 'https://music.163.com/#/discover/toplist?id=5453912201'
# 1. 发送请求
response = requests.get(url=url)
# <Response [200]>: 请求成功
# 2. 获取数据
html_data = response.text
# 3. 解析数据
# 音乐id 音乐名称 获取下来
# 正则
# <li><a href="/song\?id=(.*?)">(.*?)</a></li>
music_info = re.findall('<li><a href="/song\?id=(.*?)">(.*?)</a></li>', html_data)
for info in music_info:
    music_id = info[0]
    music_name = info[1]
    # 找不到的 别人写的代码里面抠出来
    music_url = f'http://music.163.com/song/media/outer/url?id={music_id}'
    music_name = re.sub('[\\/:*?"<>|]', '', music_name)
    print(music_url)
    # 4. 保存数据
    music_data = requests.get(url=music_url).content
    with open(f'music/{music_name}.mp3', mode='wb') as f:
        f.write(music_data)