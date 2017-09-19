import requests
from bs4 import BeautifulSoup
import sqlite3 as lite
from multiprocessing import Pool
from datetime import datetime,timedelta
import io
from PIL import Image
import hashlib

def get_gif(num):
    url = 'http://neihan1024.com/weibofun/weixin/article.php?fid={}&category=weibo_pics&source=1'.format(num)
    try:
        res = requests.get(url,timeout=5)
        soup = BeautifulSoup(res.text,'lxml')
        if soup.select('p > img') != [] :
            img_url = soup.select('p > img')[0].get('src')
            if 'sinaimg' not in img_url:
                pass
            else:
                res2 = requests.get(img_url,timeout=5)
                if res2.history:
                    pass
                else:
                    pic_size = len(res2.content)
                    hashcode=get_hash(res2.content)
                    types = img_url.split('.')[-1]
                    if 'gif' in types:
                        image_bytes = res2.content
                        data_stream = io.BytesIO(image_bytes)
                        image = Image.open(data_stream)
                        try:
                            image.seek(1)
                            category = 'gif'
                        except:
                            category = 'error'
                    else:
                        category = 'pic'
                    if category !='error':
                        title = soup.select('p')[0].text.strip()
                        created_time = soup.select('div.info_text')[0].text[:10]
                        today = str(datetime.now().date())
                        # days_later = str(datetime.now().date()+timedelta(days=30))
                        # if created_time > days_later:
                        #     created_time = today
                        #     hidden =1
                        if created_time >today:
                            created_time = today
                            hidden=0
                        else:
                            hidden=0
                        pic_index = 'neihantupian-{}'.format('0'*(6-len(str(num)))+str(num))
                        likes = int(soup.select('body > div:nth-of-type(2)')[0].text.split('\xa0')[0].strip('赞'))
                        result = save_to_sqlite(title,img_url,created_time,likes,category,pic_index,hidden,pic_size,hashcode)
                        print(num,result)
                        # print(title,img_url,created_time,likes,category,pic_index,hidden,pic_size)
                    else:
                        print(num,'gif error')
        else:
            pass
    except Exception as e:
        print(num,e)


def save_to_sqlite(title,url,created_time,likes,category,pic_index,hidden,pic_size,hashcode):
    with lite.connect('db.sqlite3') as con:
        cur = con.cursor()
        select = "SELECT * FROM pics_pics WHERE hashcode='{}'".format(hashcode)
        cur.execute(select)
        res = cur.fetchall()
        if len(res) >0:
            try:
                update = "UPDATE pics_pics set likes={} , created_time='{}' , pic_size = {} ,\
                          url = '{}' , category = '{}' ,title='{}' ,hidden={} ,pic_index = '{}' WHERE hashcode = '{}'"\
                          .format(likes,created_time,pic_size,url,category,title,hidden,pic_index,hashcode)
                cur.execute(update)
                return 'updated'
            except Exception as e:
                print('update error')
                print(e)
        else:
            try:
                insert = "INSERT INTO pics_pics (title, url, created_time,likes,category,pic_index,hidden,pic_size,hashcode) VALUES (?,?,?,?,?,?,?,?,?)"
                cur.execute(insert,(title,url,created_time,likes,category,pic_index,hidden,pic_size,hashcode))
                return 'inserted'
            except:
                print('insert error')

def get_hash(content):
    md5 = hashlib.md5()
    md5.update(content)
    return md5.hexdigest()

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
    pool.map(get_gif,range(latest-100,latest+100))
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


