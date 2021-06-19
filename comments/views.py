from django.shortcuts import render
from blog.models import  Post
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.contrib import messages
from .forms import CommentForm

@require_POST
def comment(request,post_pk):
    post = get_object_or_404(Post,pk=post_pk)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
        messages.add_message(request,messages.SUCCESS,'评论发表成功',extra_tags='success')
        return redirect(post)
    context = {
        'post': post,
        'form': form,
    }
    return render(request,'comments/preview.html',context=context)