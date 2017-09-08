import requests
from bs4 import BeautifulSoup
import sqlite3 as lite
from multiprocessing import Pool
from datetime import datetime,timedelta


def get_gif(num):
    url = 'http://neihan1024.com/weibofun/weixin/article.php?fid={}&category=weibo_pics&source=1'.format(num)
    try:
        res = requests.get(url,timeout=5)
        soup = BeautifulSoup(res.text,'lxml')
        if soup.select('p > img') != [] :
            img_url = soup.select('p > img')[0].get('src')
            res2 = requests.get(img_url,timeout=5)
            if res2.history or res.status_code != 200:
                pass
            else:
                pic_size = len(res2.content)
                types = img_url.split('.')[-1]
                if 'gif' in types:\
                    category ='gif'
                else:
                    category = 'pic'
                title = soup.select('p')[0].text.strip()
                created_time = soup.select('div.info_text')[0].text[:10]
                today = str(datetime.now().date())
                days_later = str(datetime.now().date()+timedelta(days=30))
                if created_time > days_later:
                    created_time = today
                    hidden =1
                elif created_time >today:
                    created_time = today
                    hidden=0
                else:
                    hidden=0
                pic_index = 'neihantupian-{}'.format('0'*(6-len(str(num)))+str(num))
                likes = int(soup.select('body > div:nth-of-type(2)')[0].text.split('\xa0')[0].strip('赞'))
                result = save_to_sqlite(title,img_url,created_time,likes,category,pic_index,hidden,pic_size)
                print(num,result)
                # print(title,img_url,created_time,likes,category,pic_index,hidden,pic_size)
        else:
            pass
    except Exception as e:
        print(num,e)


def save_to_sqlite(title,url,created_time,likes,category,pic_index,hidden,pic_size):
    with lite.connect('db.sqlite3') as con:
        cur = con.cursor()
        select = "SELECT * FROM pics_pics WHERE pic_index='{}'".format(pic_index)
        cur.execute(select)
        res = cur.fetchall()
        if len(res) >0:
            try:
                update = "UPDATE pics_pics set likes={} , created_time='{}' , pic_size = {} ,\
                          url = '{}' , category = '{}' ,title='{}' ,hidden={} WHERE pic_index = '{}'"\
                          .format(likes,created_time,pic_size,url,category,title,hidden,pic_index)
                cur.execute(update)
                return '更新成功'
            except Exception as e:
                print('更新失败')
                print(e)
        else:
            try:
                insert = "INSERT INTO pics_pics (title, url, created_time,likes,category,pic_index,hidden,pic_size) VALUES (?,?,?,?,?,?,?,?)"
                cur.execute(insert,(title,url,created_time,likes,category,pic_index,hidden,pic_size))
                return '插入成功'
            except:
                print('插入失败')


def latest_get():
    with lite.connect('db.sqlite3') as con:
        cur = con.cursor()
        cur.execute("select max(pic_index) from pics_pics")
        res = cur.fetchone()[0]
        latest_get_index = int(res.split('-')[1])
        return latest_get_index

if __name__ == '__main__':
    pool = Pool()
    latest = latest_get()
    print(latest)
    pool.map(get_gif,range(latest-500,latest+500))
    # pool.map(get_gif, range(160000, 179000))









# 补齐
# index_list = []
# with lite.connect('db.sqlite3') as con:
#     cur = con.cursor()
#     cur.execute("select * from pics_pics")
#     res= cur.fetchall()
#     for i in res:
#         if i[7]:
#             pic_index = int(i[7].split('-')[1])
#             if 170000 <= pic_index <=180000:
#                 index_list.append(pic_index)
#
# go_list = list(set(range(170000,180000))-set(index_list))
#
# if __name__ == '__main__':
#     pool = Pool()
#     pool.map(get_gif,go_list)



# from pics.models import Pics
# import sqlite3 as lite
#
# for i in Pics.objects.all():
#     with lite.connect('db.sqlite3') as con:
#         cur = con.cursor()
#         cur.execute("select * from neihan where (url ='{}' and title = '{}')".format(i.url,i.title))
#         res = cur.fetchone()
#         if res:
#             i.likes = res[3]
#             i.save()
#             print(i.title,i.likes)


