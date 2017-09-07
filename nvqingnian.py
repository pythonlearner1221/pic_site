import requests
from bs4 import BeautifulSoup
import re
import sqlite3 as lite
from datetime import datetime

def daily_pics():
    index = 'http://www.nvqingnian.net/new/'
    try:
        mres=requests.get(index)
        msoup = BeautifulSoup(mres.text, 'lxml')
        parts = msoup.select('div.newspic01')[0].select('a')[0].get('href')
        link = 'http://www.nvqingnian.net/'+parts
        print(link)
        res = requests.get(link)
        soup=BeautifulSoup(res.text,'lxml')
        index1 = re.search(r'「(\d+)」福利', res.text, re.S).group(1)
        index2 = str(int(index1) + 1)
        img_inside = '「{}」(.*?)「{}」'.format(index1, index2)
        imgtext = re.search(img_inside, res.text, re.S).group(1)
        img_links = re.findall('img src="(.*?)"', imgtext, re.S)
        gif_links = re.findall(r'[a-zA-z]+://[^\s]*.gif', res.text, re.S)

        for i in img_links:
            if i.split('.')[-1] !='gif':
                save_to_sqlite('福利', i,'pic')
            else:
                pass
        print('保存',len(img_links),'福利图')
        # gif_links=[i.get('src') for i in soup.select('img') if 'gif' in i.get('src') and 'static' not in i.get('src') and 'template' not in i.get('src')]
        for j in gif_links:
            save_to_sqlite('动图', j,'gif')
        print('保存',len(gif_links),'动图')
    except:
        pass

def save_to_sqlite(title,url,category):
    with lite.connect('db.sqlite3') as con:
        cur = con.cursor()
        select = "SELECT * FROM pics_pics WHERE (title='{}' and url = '{}')".format(title,url)
        cur.execute(select)
        res = cur.fetchall()
        created_time=datetime.now().date()
        likes=0
        hidden=1
        if len(res) ==0:
            try:
                insert = "INSERT INTO pics_pics (title, url, created_time,likes,category,hidden) VALUES (?,?,?,?,?,?)"
                cur.execute(insert, (title, url,created_time,likes,category,hidden))
                return 'inserted'
            except Exception as e:
                print('failed')
                print(e)
        else:
            pass


daily_pics()