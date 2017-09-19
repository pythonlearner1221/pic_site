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

def get_dailypost(xyz):
    today = datetime.now().date()
    day = today - timedelta(days=xyz)
    cat = Category.objects.get(id=1)  # 每日一模
    tag1= Tags.objects.get(name='妹子图片')
    tag2 = Tags.objects.get(name='妹子动图')
    try:
        if len(DailyPost.objects.filter(created_time=day,category=cat))==0:
            if len(Pics.objects.filter(created_time=day))>=30:
                post_list = []

                ####likes
                gifs = Pics.objects.filter(created_time=day, category='gif').order_by('-likes')
                pics = Pics.objects.filter(created_time=day, category='pic').order_by('-likes')
                if len(gifs) < 15:
                    post_list.extend(gifs)
                    post_list.extend(pics[0:(30-len(gifs))])

                elif len(pics) < 15:
                    post_list.extend(gifs[0:(30 - len(pics))])
                    post_list.extend(pics)

                # elif len(pics)>40 and len(gifs)>40:
                #     post_list.extend(random.sample(gifs[:30], k=15))
                #     post_list.extend(random.sample(pics[:30], k=15))

                else:
                    post_list.extend(gifs[0:15])
                    post_list.extend(pics[0:15])

                title = post_list[1].title
                for i in range(0,30):
                    if 15<=len(post_list[i].title)< 25:
                        title = post_list[i].title
                        break
                    if len(post_list[i].title) >=25:
                        title = post_list[i].title[:20]+'...'
                        break

                # views=int(sum([i.likes for i in post_list])/100)
                views = random.choice(range(1000, 2000))
                try:
                    created_time = gifs[0].created_time
                except:
                    created_time = pics[0].created_time
                body = ''
                for i in range(0,30):
                    text = '#### 【{}】{}\n![]({})\n'.format((i+1),post_list[i].title,post_list[i].url)
                    body+=text
                fuli = [i.url for i in random.sample(list(Pics.objects.filter(~Q(created_time=day),tags=tag1,)),k=4)]
                dongtu =[i.url for i in random.sample(list(Pics.objects.filter(~Q(created_time=day),tags=tag2)),k=4)]
                fuli_text = '#### 【31】每日福利\n'
                for i in fuli:
                    fuli_text+='![]('+i+')\n\n'
                for i in dongtu:
                    fuli_text+='![]('+i+')\n\n'
                body = body+fuli_text

                body_for_cl=''
                for i in range(0,30):
                    text = '【{}】{}\n[img]{}[/img]\n'.format((i+1),post_list[i].title,post_list[i].url)
                    body_for_cl+=text
                fuli_for_cl='【31】每日福利\n'
                for i in fuli:
                    fuli_for_cl+='[img]'+i+'[/img]\n\n'
                for i in dongtu:
                    fuli_for_cl+='[img]'+i+'[/img]\n\n'
                body_for_cl=body_for_cl+fuli_for_cl
                path = 'static/for_cl/for_cl.txt'
                title_for_cl = '[每日一莫'+today.strftime('%Y%m%d')[2:]+']'+''.join(re.split(r'[【】]',title))+'\n\n'
                with open(path,'w',encoding='utf-8') as f:
                    f.write(title_for_cl)
                    f.write(body_for_cl)
                # print(body_for_cl)
                image=fuli[0]
                c= DailyPost()
                c.title=title
                c.created_time=created_time
                c.body=body
                c.image=image
                user = User.objects.get(username='toosiki')
                cat = Category.objects.get(id=1)
                c.category=cat
                c.author=user
                c.views = views
                c.save()
                print(created_time,'saved')
            else:
                print('资源太少，凑不够一篇文章')
        else:
            print('今天的一莫已经更新了，别催更了')
    except Exception as e:
        print('save', day, 'failed')
        print(e)

def get_weixinpost(xyz):
    today = datetime.now().date()
    day = today - timedelta(days=xyz)
    tag1 = Tags.objects.get(name='妹子图片')
    tag2 = Tags.objects.get(name='妹子动图')
    try:
        if len(HiddenPost.objects.filter(created_time=day, category='微信一莫')) == 0:
            if len(Pics.objects.filter(created_time=day,pic_size__lt=2000000,pic_size__gt=0,hidden=0)) >= 30:
                post_list = []

                ####likes
                gifs = Pics.objects.filter(created_time=day, category='gif',pic_size__lt=2000000,pic_size__gt=0,hidden=0).order_by('-likes')
                pics = Pics.objects.filter(created_time=day, category='pic',pic_size__lt=2000000,pic_size__gt=0,hidden=0).order_by('-likes')
                if len(gifs) < 15:
                    post_list.extend(gifs)
                    post_list.extend(pics[0:(30 - len(gifs))])

                elif len(pics) < 15:
                    post_list.extend(gifs[0:(30 - len(pics))])
                    post_list.extend(pics)

                # elif len(pics) > 40 and len(gifs) > 40:
                #     post_list.extend(random.sample(gifs[:30], k=15))
                #     post_list.extend(random.sample(pics[:30], k=15))

                else:
                    post_list.extend(gifs[0:15])
                    post_list.extend(pics[0:15])

                title = post_list[1].title
                for i in range(0, 30):
                    if 15 <= len(post_list[i].title) < 25:
                        title = post_list[i].title
                        break
                    if len(post_list[i].title) >= 25:
                        title = post_list[i].title[:20] + '...'
                        break

                # views=int(sum([i.likes for i in post_list])/100)
                views = random.choice(range(1000, 2000))
                try:
                    created_time = gifs[0].created_time
                except:
                    created_time = pics[0].created_time
                body = ''
                for i in range(0, 30):
                    text = '#### 【{}】{}\n![]({})\n'.format((i + 1), post_list[i].title, post_list[i].url)
                    body += text
                fuli = [i.url for i in random.sample(list(Pics.objects.filter(~Q(created_time=day), tags=tag1, )), k=4)]
                dongtu = [i.url for i in random.sample(list(Pics.objects.filter(~Q(created_time=day), tags=tag2)), k=4)]
                fuli_text = '#### 【31】每日福利\n'
                for i in fuli:
                    fuli_text += '![](' + i + ')\n\n'
                for i in dongtu:
                    fuli_text += '![](' + i + ')\n\n'
                body = body + fuli_text

                title = '[每日一莫' + created_time.strftime('%y%m%d') + ']' + title

                image = fuli[0]
                c = HiddenPost()
                c.title = title
                c.created_time = created_time
                c.body = body
                c.image = image
                c.category = '微信一莫'
                c.save()
                print(c.category,created_time, 'saved')
            else:
                print('资源太少，凑不够一篇微信文章')
        else:
            print('今天的微信一莫已经更新了，别催更了')
    except Exception as e:
        print('save', day, 'failed')
        print(e)

def get_toutiaopost(xyz):
    today = datetime.now().date()
    day = today - timedelta(days=xyz)
    tag1 = Tags.objects.get(name='妹子图片')
    try:
        if len(HiddenPost.objects.filter(created_time=day, category='头条一莫')) == 0:
            if len(Pics.objects.filter(created_time=day,hidden=0)) >= 30:
                post_list = []

                ####likes
                gifs = Pics.objects.filter(created_time=day, category='gif',hidden=0).order_by('-likes')
                pics = Pics.objects.filter(created_time=day, category='pic',hidden=0).order_by('-likes')
                if len(gifs) < 15:
                    post_list.extend(gifs)
                    post_list.extend(pics[0:(30 - len(gifs))])

                elif len(pics) < 15:
                    post_list.extend(gifs[0:(30 - len(pics))])
                    post_list.extend(pics)

                elif len(pics) > 40 and len(gifs) > 40:
                    post_list.extend(random.sample(gifs[:30], k=15))
                    post_list.extend(random.sample(pics[:30], k=15))

                else:
                    post_list.extend(gifs[0:15])
                    post_list.extend(pics[0:15])

                title = post_list[1].title
                for i in range(0, 30):
                    if 15 <= len(post_list[i].title) < 25:
                        title = post_list[i].title
                        break
                    if len(post_list[i].title) >= 25:
                        title = post_list[i].title[:20] + '...'
                        break

                # views=int(sum([i.likes for i in post_list])/100)
                views = random.choice(range(1000, 2000))
                try:
                    created_time = gifs[0].created_time
                except:
                    created_time = pics[0].created_time
                body = ''
                for i in range(0, 30):
                    text = '#### 【{}】{}\n![]({})\n'.format((i + 1), post_list[i].title, post_list[i].url)
                    body += text

                # print(body_for_cl)

                title = '[每日一莫' + created_time.strftime('%y%m%d') + ']' + title
                image = random.choice(Pics.objects.filter(~Q(created_time=day), tags=tag1, )).url
                c = HiddenPost()
                c.title = title
                c.created_time = created_time
                c.body = body
                c.image = image
                c.category = '头条一莫'
                c.save()
                print(c.category,created_time, 'saved')
            else:
                print('资源太少，凑不够一篇头条')
        else:
            print('今天的头条一莫已经更新了，别催更了')
    except Exception as e:
        print('save', day, 'failed')
        print(e)

# if __name__=='__main__':
#     for i in range(1,15):
#         get_dailypost(i)
#         get_weixinpost(i)

# for i in range(1876,1,-1):
#     get_dailypost(i)


if __name__ == '__main__':
    get_dailypost(1)
    get_weixinpost(1)
    get_toutiaopost(1)
