import sys,os
import django
pro_dir = os.getcwd()  #如果放在project目录，就不需要在配置绝对路径了
sys.path.append(pro_dir)
os.environ['DJANGO_SETTINGS_MODULE'] ='pic_site.settings'  #项目的settings
django.setup()
from pics.models import Pics,Tags
from dailypost.models import DailyPost,Category
from datetime import datetime,timedelta
import random
from django.contrib.auth.models import User
from multiprocessing import Pool


# for xyz in range(1868,1,-1):
def weekly_best(xyz):
    today = datetime.now().date()
    last_sunday = today-timedelta(days=(7*(xyz-1)+today.isoweekday()))
    last_monday = last_sunday-timedelta(days=6)
    monday= last_sunday+timedelta(days=1)
    cat = Category.objects.get(id=2)  # 一周最佳
    tag1 = Tags.objects.get(name='妹子图片')
    try:
        if len(DailyPost.objects.filter(created_time=monday,category=cat)) ==0:
            if len(Pics.objects.filter(created_time__gte=last_monday,created_time__lte=last_sunday,hidden=0))>=50:
                post_list = []
                gifs = Pics.objects.filter(created_time__gte=last_monday,created_time__lte=last_sunday, category='gif',hidden=0).order_by('-likes')
                pics = Pics.objects.filter(created_time__gte=last_monday,created_time__lte=last_sunday, category='pic',hidden=0).order_by('-likes')
                if len(gifs) < 25:
                    post_list.extend(pics[0:(50-len(gifs))])
                    post_list.extend(gifs)
                elif len(pics) < 25:
                    post_list.extend(pics)
                    post_list.extend(gifs[0:(50-len(pics))])
                else:
                    post_list.extend(pics[0:25])
                    post_list.extend(gifs[0:25])


                title = post_list[1].title
                for i in range(0,50):
                    if 15<=len(post_list[i].title)< 25:
                        title = post_list[i].title
                        break
                    if len(post_list[i].title) >=25:
                        title = post_list[i].title[:20]+'...'
                        break

                # views=int(sum([i.likes for i in post_list])/100)
                views = random.choice(range(1000,2000))
                created_time = monday
                body = ''
                for i in range(0,50):
                    text = '#### 【{}】{}\n![]({})\n'.format((i+1),post_list[i].title,post_list[i].url)
                    body+=text

                fuli = [i.url for i in random.choices(Pics.objects.filter(tags=tag1),k=1)]
                # dongtu =[i.url for i in random.choices(FuLi.objects.filter(title='动图'),k=4)]
                # fuli_text,dongtu_text = '#### 【31】福利\n','### 【32】动图\n'
                # for i in fuli:
                #     fuli_text+='![]('+i+')\n\n'
                # for i in dongtu:
                #     dongtu_text+='![]('+i+')\n\n'
                # body = body+fuli_text+dongtu_text
                image=fuli[0]
                c= DailyPost()
                c.title=title
                c.created_time=created_time
                c.body=body
                c.image=image
                user = User.objects.get(username='toosiki')
                cat = Category.objects.get(id=2)
                c.category=cat
                c.author=user
                c.views = views
                c.save()
                print(last_sunday,'saved')
            else:
                print('资源太少，凑不够一篇文章')
        else:
            print('没到周一，急什么急')
    except Exception as e:
        print('save', last_sunday, 'failed')
        print(e)


# if __name__=='__main__':
#     pool=Pool()
#     pool.map(get_dailypost,range(1,2))

# for i in range(267,0,-1):
#     weekly_best(i)

weekly_best(1)