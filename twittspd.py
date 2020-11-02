import urllib.request,urllib.parse,urllib.error
import ssl
import json
import digsign
import sqlite3
# establish connection to database
conn=sqlite3.connect('twittspd.sqlite')
cur=conn.cursor()
cur.execute('drop table if exists twitter')
cur.execute('''create table twitter(name text,retrieved integer,friend integer)''')
tw='https://api.twitter.com/1.1/friends/list.json'
#ignore ssl certification errors
ctx=ssl.create_default_context()
ctx.check_hostname=False
ctx.verify_mode=ssl.CERT_NONE
while True:
    scrnm=input('enter screen name')
    if scrnm=='quit':break
    curs=-1
    while curs!=0:
        url=digsign.augment(tw,{'screen_name':scrnm,'cursor':curs})
        print(url)
        connection=urllib.request.urlopen(url,context=ctx)
        data=connection.read().decode()
        js=json.loads(data)
        #print(json.dumps(js,indent=2))
        for i in js['users']:
                print(i['screen_name'])
                frnd=i['screen_name']
                cur.execute('insert into twitter(name,friend)values(?,1)',(frnd,))
                conn.commit()
        head=dict(connection.getheaders())
        print(head['x-rate-limit-remaining'])
        curs=js['next_cursor'] # we use cursoring to show complete list of friends using cursor argument 
cur.close()
