from django.shortcuts import render,get_object_or_404,redirect
import  markdown,re
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension
from .models import Post,Category,Tag
from django.http import HttpResponse
from django.views.generic import ListView,DetailView #使用类视图
#from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from pure_pagination import PaginationMixin, Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.db.models import Q

# Create your views here.

class IndexView(PaginationMixin,ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    paginate_by = 10

class CategoryView(IndexView):
    def get_queryset(self):
         cate = get_object_or_404(Category,pk=self.kwargs.get('pk'))
         return super().get_queryset().filter(category=cate)

class TagView(IndexView):
    def get_queryset(self):
        t = get_object_or_404(Tag, pk=self.kwargs.get("pk"))
        return super().get_queryset().filter(tags=t)

class ArchiveView(IndexView):
    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        return  super(ArchiveView,self).get_queryset().filter(create_time__year=year,create_time__month=month)

class PostDetaiView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'
    def get(self, request, *args, **kwargs):
        response = super(PostDetaiView,self).get(request, *args, **kwargs)
        self.object.increase_views()
        return response

def search(request):
    q = request.GET.get('q')
    if not q:
        error_msg = '请输入关键词进行搜索'
        meaaages.add_message(request,messages.ERROR, error_msg,extra_tags='danger')
        return redirect('blog:index')
    post_list = Post.objects.filter(Q(title__icontains=q) | Q(body__icontains=q))
    return render(request,'blog/index.html',{'post_list': post_list})
'''
    def get_object(self,queryset=None):
        post = super().get_object(queryset=None)
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            TocExtension(slugify=slugify)
        ])
        post.body = md.convert(post.body)
        m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc,re.S)
        post.toc = m.group(1) if m is not  None else ''
        return post
'''

'''
def detail(request,pk):
    post = get_object_or_404(Post,pk=pk)
    post.increase_views()
    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',  # toc 是自动生成目录的扩展
       # TocExtension(slugify=slugify),
    ])
    post.body = md.convert(post.body)
    #post.toc = md.toc
    m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>',md.toc,re.S)
    post.toc = m.group(1) if m is not None else ''
    print(post.body)
    print(post.toc)
    return render(request,'blog/detail.html',context={'post':post})


def archive(request, year, month):
    post_list = Post.objects.filter(create_time__year=year,
                                    create_time__month=month).order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})

def index(request):
    post_list = Post.objects.all().order_by('-create_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})

def category(request,pk):
    cate = get_object_or_404(Category,pk=pk)
    post_list = Post.objects.filter(category=cate).order_by('-create_time')
    return render(request,'blog/index.html',context={'post_list':post_list})

def tag(request,pk):
    t=get_object_or_404(Tag,pk=pk)
    post_list = Post.objects.filter(tags=t).order_by('-create_time')
    return render(request,'blog/index.html',context={'post_list':post_list})

def test(request):
    return render(request,'blog/detail.html')
    
'''