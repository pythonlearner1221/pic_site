from django.shortcuts import render
from .models import Pics,Tags
from django.views.generic import ListView
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
import random
from datetime import datetime,timedelta
# Create your views here.

# def index(request):
#     pics = GifPics.objects.all().order_by('-gif_index')
#     return render(request,'index.html',context={'pics':pics})

class IndexView(ListView):
    model = Pics
    template_name = 'pics/index.html'
    context_object_name = 'pics'
    paginate_by = 10
    ordering=['-created_time','-id']

    # def get_queryset(self):
    #     return super(IndexView,self).get_queryset().filter(hidden=0)

    def get_context_data(self, **kwargs):
        """
        在视图函数中将模板变量传递给模板是通过给 render 函数的 context 参数传递一个字典实现的，
        例如 render(request, 'blog/index.html', context={'post_list': post_list})，
        这里传递了一个 {'post_list': post_list} 字典给模板。
        在类视图中，这个需要传递的模板变量字典是通过 get_context_data 获得的，
        所以我们复写该方法，以便我们能够自己再插入一些我们自定义的模板变量进去。
        """

        # 首先获得父类生成的传递给模板的字典。
        context = super().get_context_data(**kwargs)

        # 父类生成的字典中已有 paginator、page_obj、is_paginated 这三个模板变量，
        # paginator 是 Paginator 的一个实例，
        # page_obj 是 Page 的一个实例，
        # is_paginated 是一个布尔变量，用于指示是否已分页。
        # 例如如果规定每页 10 个数据，而本身只有 5 个数据，其实就用不着分页，此时 is_paginated=False。
        # 关于什么是 Paginator，Page 类在 Django Pagination 简单分页：http://zmrenwu.com/post/34/ 中已有详细说明。
        # 由于 context 是一个字典，所以调用 get 方法从中取出某个键对应的值。
        paginator = context.get('paginator')
        page = context.get('page_obj')
        is_paginated = context.get('is_paginated')

        # 调用自己写的 pagination_data 方法获得显示分页导航条需要的数据，见下方。
        pagination_data = self.pagination_data(paginator, page, is_paginated)

        # 将分页导航条的模板变量更新到 context 中，注意 pagination_data 方法返回的也是一个字典。
        context.update(pagination_data)

        # 将更新后的 context 返回，以便 ListView 使用这个字典中的模板变量去渲染模板。
        # 注意此时 context 字典中已有了显示分页导航条所需的数据。
        return context

    def pagination_data(self, paginator, page, is_paginated):
        if not is_paginated:
            # 如果没有分页，则无需显示分页导航条，不用任何分页导航条的数据，因此返回一个空的字典
            return {}

        # 当前页左边连续的页码号，初始值为空
        left = []

        # 当前页右边连续的页码号，初始值为空
        right = []

        # 标示第 1 页页码后是否需要显示省略号
        left_has_more = False

        # 标示最后一页页码前是否需要显示省略号
        right_has_more = False

        # 标示是否需要显示第 1 页的页码号。
        # 因为如果当前页左边的连续页码号中已经含有第 1 页的页码号，此时就无需再显示第 1 页的页码号，
        # 其它情况下第一页的页码是始终需要显示的。
        # 初始值为 False
        first = False

        # 标示是否需要显示最后一页的页码号。
        # 需要此指示变量的理由和上面相同。
        last = False

        # 获得用户当前请求的页码号
        page_number = page.number

        # 获得分页后的总页数
        total_pages = paginator.num_pages

        # 获得整个分页页码列表，比如分了四页，那么就是 [1, 2, 3, 4]
        page_range = paginator.page_range

        if page_number == 1:
            # 如果用户请求的是第一页的数据，那么当前页左边的不需要数据，因此 left=[]（已默认为空）。
            # 此时只要获取当前页右边的连续页码号，
            # 比如分页页码列表是 [1, 2, 3, 4]，那么获取的就是 right = [2, 3]。
            # 注意这里只获取了当前页码后连续两个页码，你可以更改这个数字以获取更多页码。
            right = page_range[page_number:page_number + 2]

            # 如果最右边的页码号比最后一页的页码号减去 1 还要小，
            # 说明最右边的页码号和最后一页的页码号之间还有其它页码，因此需要显示省略号，通过 right_has_more 来指示。
            if right[-1] < total_pages - 1:
                right_has_more = True

            # 如果最右边的页码号比最后一页的页码号小，说明当前页右边的连续页码号中不包含最后一页的页码
            # 所以需要显示最后一页的页码号，通过 last 来指示
            if right[-1] < total_pages:
                last = True

        elif page_number == total_pages:
            # 如果用户请求的是最后一页的数据，那么当前页右边就不需要数据，因此 right=[]（已默认为空），
            # 此时只要获取当前页左边的连续页码号。
            # 比如分页页码列表是 [1, 2, 3, 4]，那么获取的就是 left = [2, 3]
            # 这里只获取了当前页码后连续两个页码，你可以更改这个数字以获取更多页码。
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]

            # 如果最左边的页码号比第 2 页页码号还大，
            # 说明最左边的页码号和第 1 页的页码号之间还有其它页码，因此需要显示省略号，通过 left_has_more 来指示。
            if left[0] > 2:
                left_has_more = True

            # 如果最左边的页码号比第 1 页的页码号大，说明当前页左边的连续页码号中不包含第一页的页码，
            # 所以需要显示第一页的页码号，通过 first 来指示
            if left[0] > 1:
                first = True
        else:
            # 用户请求的既不是最后一页，也不是第 1 页，则需要获取当前页左右两边的连续页码号，
            # 这里只获取了当前页码前后连续两个页码，你可以更改这个数字以获取更多页码。
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
            right = page_range[page_number:page_number + 2]

            # 是否需要显示最后一页和最后一页前的省略号
            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True

            # 是否需要显示第 1 页和第 1 页后的省略号
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True

        data = {
            'left': left,
            'right': right,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'first': first,
            'last': last,
        }

        return data

class HiddenView(IndexView):
    def get_queryset(self):
        return super(IndexView,self).get_queryset().filter(hidden=1)



class ArchivesView(IndexView):
    def get_queryset(self):
        year= self.kwargs.get('year')
        month=self.kwargs.get('month')
        return super(ArchivesView,self).get_queryset().filter(created_time__year=year,created_time__month=month)

class ArchivesYearView(IndexView):
    def get_queryset(self):
        year= self.kwargs.get('year')
        return super(ArchivesYearView,self).get_queryset().filter(created_time__year=year)

class CategoryView(IndexView):
    def get_queryset(self):
        category= self.kwargs.get('category')
        if category == 'pics':
            pic_type= 'pic'
        else :
            pic_type= 'gif'
        return super(CategoryView,self).get_queryset().filter(category=pic_type)

def search(request):
    q=request.GET.get('q')

    page = request.GET.get('page')

    if not page:
        page=1


    error_msg=''
    if not q:
        error_msg='请输入关键词'
        return render(request, 'pics/search.html', {'error_msg':error_msg})

    pic_list = Pics.objects.filter(Q(title__icontains=q)).order_by('-created_time')


    paginator = Paginator(pic_list, 10)

    if len(pic_list) > 10:
        is_paginated = True
    else:
        is_paginated = False

    # 当前页左边连续的页码号，初始值为空
    left = []

    # 当前页右边连续的页码号，初始值为空
    right = []

    # 标示第 1 页页码后是否需要显示省略号
    left_has_more = False

    # 标示最后一页页码前是否需要显示省略号
    right_has_more = False

    # 标示是否需要显示第 1 页的页码号。
    # 因为如果当前页左边的连续页码号中已经含有第 1 页的页码号，此时就无需再显示第 1 页的页码号，
    # 其它情况下第一页的页码是始终需要显示的。
    # 初始值为 False
    first = False

    # 标示是否需要显示最后一页的页码号。
    # 需要此指示变量的理由和上面相同。
    last = False

    # 获得用户当前请求的页码号
    page_number = int(page)

    # 获得分页后的总页数
    total_pages = paginator.num_pages

    # 获得整个分页页码列表，比如分了四页，那么就是 [1, 2, 3, 4]
    page_range = paginator.page_range

    if page_number == 1:
        # 如果用户请求的是第一页的数据，那么当前页左边的不需要数据，因此 left=[]（已默认为空）。
        # 此时只要获取当前页右边的连续页码号，
        # 比如分页页码列表是 [1, 2, 3, 4]，那么获取的就是 right = [2, 3]。
        # 注意这里只获取了当前页码后连续两个页码，你可以更改这个数字以获取更多页码。
        right = page_range[page_number:page_number + 2]

        # 如果最右边的页码号比最后一页的页码号减去 1 还要小，
        # 说明最右边的页码号和最后一页的页码号之间还有其它页码，因此需要显示省略号，通过 right_has_more 来指示。
        if right[-1] < total_pages - 1:
            right_has_more = True

        # 如果最右边的页码号比最后一页的页码号小，说明当前页右边的连续页码号中不包含最后一页的页码
        # 所以需要显示最后一页的页码号，通过 last 来指示
        if right[-1] < total_pages:
            last = True

    elif page_number == total_pages:
        # 如果用户请求的是最后一页的数据，那么当前页右边就不需要数据，因此 right=[]（已默认为空），
        # 此时只要获取当前页左边的连续页码号。
        # 比如分页页码列表是 [1, 2, 3, 4]，那么获取的就是 left = [2, 3]
        # 这里只获取了当前页码后连续两个页码，你可以更改这个数字以获取更多页码。
        left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]

        # 如果最左边的页码号比第 2 页页码号还大，
        # 说明最左边的页码号和第 1 页的页码号之间还有其它页码，因此需要显示省略号，通过 left_has_more 来指示。
        if left[0] > 2:
            left_has_more = True

        # 如果最左边的页码号比第 1 页的页码号大，说明当前页左边的连续页码号中不包含第一页的页码，
        # 所以需要显示第一页的页码号，通过 first 来指示
        if left[0] > 1:
            first = True
    else:
        # 用户请求的既不是最后一页，也不是第 1 页，则需要获取当前页左右两边的连续页码号，
        # 这里只获取了当前页码前后连续两个页码，你可以更改这个数字以获取更多页码。
        left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:(page_number - 1)]
        right = page_range[page_number:(page_number + 2)]

        # 是否需要显示最后一页和最后一页前的省略号
        if right[-1] < total_pages - 1:
            right_has_more = True
        if right[-1] < total_pages:
            last = True

        # 是否需要显示第 1 页和第 1 页后的省略号
        if left[0] > 2:
            left_has_more = True
        if left[0] > 1:
            first = True

    try:
        pics = paginator.page(page)
    except PageNotAnInteger:
        # 如果用户请求的页码号不是整数，显示第一页
        pics = paginator.page(1)
    except EmptyPage:
        # 如果用户请求的页码号超过了最大页码号，显示最后一页
        pics = paginator.page(paginator.num_pages)

    return render(request, 'pics/search.html', {'error_msg':error_msg, 'pics':pics, 'q':q, 'is_paginated':is_paginated,
                                              'left': left,
                                              'right': right,
                                              'left_has_more': left_has_more,
                                              'right_has_more': right_has_more,
                                              'first': first,
                                              'last': last,
                                                'page_obj':pics,
                                                'paginator':paginator
                                                })


class PrettyView(HiddenView):
    template_name = 'pics/pretty.html'
    ordering=['-created_time','-id']

class PrettyCategoryView(PrettyView):
    def get_queryset(self):
        tag1 = Tags.objects.get(name='妹子图片')
        tag2 = Tags.objects.get(name='妹子动图')
        category= self.kwargs.get('category')
        if category == 'tupian':
            pic_type= tag1
        else :
            pic_type= tag2
        return super(PrettyCategoryView,self).get_queryset().filter(tags=pic_type)

def random_post(request):
    pic = random.choice(Pics.objects.filter(hidden=1))
    return render(request,'pics/random.html',context={
        'pic':pic,
        'from':'pics:random',
        'to':''
    })

def random_category(request,category):
    tag1 = Tags.objects.get(name='妹子图片')
    tag2 = Tags.objects.get(name='妹子动图')
    if category == 'tupian':
        pic_type = tag1
    else:
        pic_type = tag2
    pic = random.choice(Pics.objects.filter(tags=pic_type))
    return render(request, 'pics/random.html', context={
        'pic': pic,
        'from':'pics:random_category',
        'to':category
    })

def choose(request):
    today = datetime.now().date()
    pic = Pics.objects.filter(hidden=0,tags__isnull=True,created_time__lt=today).order_by('created_time','id').last()
    return render(request,'pics/choose.html',context={
        'pic':pic,
    })

def choose_tag(request,tag):
    today = datetime.now().date()
    if tag =='1':
        pic = Pics.objects.filter(hidden=0,tags__isnull=True,created_time__lt=today).order_by('created_time','id').last()
        pic.hidden=1
        if pic.category == 'pic':
            pic.tags.add(Tags.objects.get(name='妹子图片'))
        if pic.category == 'gif':
            pic.tags.add(Tags.objects.get(name='妹子动图'))
        pic.created_time = datetime.now().date()-timedelta(days=1)
        pic.save()
    if tag == '0':
        pic = Pics.objects.filter(hidden=0, tags__isnull=True,created_time__lt=today).order_by('created_time','id').last()
        pic.hidden=0
        pic.tags.add(Tags.objects.get(name='其他'))
        pic.save()
    if tag == '2':
        pic = Pics.objects.filter(hidden=0, tags__isnull=True, created_time__lt=today).order_by('created_time','id').last()
        pic.delete()
    new_pic = Pics.objects.filter(hidden=0,tags__isnull=True,created_time__lt=today).order_by('created_time','id').last()
    return render(request, 'pics/choose.html', context={
        'pic': new_pic,
    })
