import sys,os
import django
pro_dir = os.getcwd()  #如果放在project目录，就不需要在配置绝对路径了
sys.path.append(pro_dir)
os.environ['DJANGO_SETTINGS_MODULE'] ='pic_site.settings'  #项目的settings
django.setup()
from pics.models import Pics,Tags
from dailypost.models import DailyPost,Category,HiddenPost
from datetime import datetime,timedelta
import random
from django.contrib.auth.models import User
import re
from django.db.models import Q
from makedailypost import get_dailypost,get_weixinpost
from neihan import get_gif,latest_get
from makeweeklybest import weekly_best


def make_weixinpost():
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    if len(Pics.objects.filter(created_time=yesterday, tags__isnull=True)) ==0:
        return True
    else :
        return False

if __name__=='__main__':
    latest = latest_get()
    for i in range(latest-500,latest+500):
        get_gif(i)
    get_dailypost(1)
    weekly_best(1)
    if make_weixinpost():
        get_weixinpost(1)
    else:
        print('昨天图片尚未分类')