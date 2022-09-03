import json

jsondata = '''
{
"Uin":0,
"UserName":"@c482d142bc698bc3971d9f8c26335c5c",
"NickName":"小帅b",
"DisplayName":"",
"ChatRoomId":0,
"KeyWord":"che",
"EncryChatRoomId":"",
"IsOwner":0
}
'''

myfriend = json.loads(jsondata)
print(myfriend.get('KeyWord'))