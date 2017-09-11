import sys,os
import django
pro_dir = os.getcwd()  #如果放在project目录，就不需要在配置绝对路径了
sys.path.append(pro_dir)
os.environ['DJANGO_SETTINGS_MODULE'] ='pic_site.settings'  #项目的settings
django.setup()
from pics.models import Pics,Tags
from datetime import datetime,timedelta
from makedailypost import get_dailypost,get_weixinpost
from neihan import get_gif,latest_get
from makeweeklybest import weekly_best
import time


def make_weixinpost():
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    if len(Pics.objects.filter(created_time=yesterday, tags__isnull=True)) ==0:
        return True
    else :
        return False

if __name__=='__main__':
    while True:
        print('开启定时任务')
        if datetime.now().hour == 12:
            latest = latest_get()
            print('昨天获取到',latest,'开始更新')
            print('开始进行旧图更新和新图获取')
            for i in range(latest-500,latest+500):
                get_gif(i)
            print('开始生成每日一莫')
            get_dailypost(1)
            print('开始生成每周最佳')
            weekly_best(1)
            print('开始生成微信每日一莫')
            if make_weixinpost():
                get_weixinpost(1)
            else:
                print('昨天图片尚未分类')

        if datetime.now().hour == 17:
            print('开始生成微信每日一莫')
            if make_weixinpost():
                get_weixinpost(1)
            else:
                print('昨天图片尚未分类')

        time.sleep(3600)