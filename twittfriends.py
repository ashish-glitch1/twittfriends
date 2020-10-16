import urllib.request,urllib.parse,urllib.error
import digsign      #digsign is environment variable
import ssl
import json
#go to https://apps.twitter.com/ and create a developer account
#click on create new app app & get the four string and put them in hidden.py
scrnm=input('enter user name')
print('calling twitter')
url=digsign.augment('https://api.twitter.com/1.1/friends/list.json',{'screen name':scrnm})
print(url)
#ignore ssl certification errors
ctx=ssl.create_default_context()
ctx.check_hostname=False
ctx.verify_mode=ssl.CERT_NONE

connection=urllib.request.urlopen(url,context=ctx)
data=connection.read().decode()
print('***************')
js=json.loads(data)
print(json.dumps(js,indent=2))
for i in js['users']:
    print(i['name'])      #this prints the friends list
    print(i['status']['text']) #this prints the latest post by that friend
print('========================')
headers=dict(connection.getheaders())
print(headers['x-rate-limit-remaining'])    #this prints the left api request u can make per 15 min
