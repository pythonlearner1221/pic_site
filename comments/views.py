from django.shortcuts import render,get_object_or_404,redirect
from dailypost.models import DailyPost
from .models import Comment
from .forms import CommentForm
import markdown
# Create your views here.


def post_comment(request,post_pk):
    post = get_object_or_404(DailyPost,pk=post_pk)

    if request.method =='POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment=form.save(commit=False)
            comment.post =post
            comment.save()
            return redirect(post)
        else:
            comment_list = post.comment_set.all()
            context = {
                'post':post,
                'form':form,
                'comment_list':comment_list
            }
            return render(request,'dailypost/detail.html',context=context)
    return redirect(post)