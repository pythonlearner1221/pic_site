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
    print('start daily task')
    latest = latest_get()
    print('latest index', latest)
    print('start updating and getting new info')
    for i in range(latest - 50, latest + 50):
        get_gif(i)
    print('start generating daily yimo')
    get_dailypost(1)
    print('start generating weekly best')
    weekly_best(1)
    print('start generating daily yimo for public')
    get_weixinpost(1)
    # if make_weixinpost():
    #     get_weixinpost(1)
    # else:
    #     print('exists unclassified yesterday\'s pics')
