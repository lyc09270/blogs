from django import template
from ..models import Post,Tag,Category
from django.db.models.aggregates import Count
from django.db.models.functions import ExtractYear,ExtractMonth

register = template.Library()
# 最新文章标签
@register.inclusion_tag('blog/inclusions/_recent_posts.html',takes_context=True)
def show_recent_posts(context,num=5):
    return {
        'recent_post_list': Post.objects.all().order_by('-create_time')[:num]
}

# 归档模板标签
@register.inclusion_tag('blog/inclusions/_archives.html',takes_context=True)
def show_archives(context):
    date_list = Post.objects.annotate(year=ExtractYear('create_time'), month=ExtractMonth('create_time')).values('year', 'month').order_by('year', 'month').annotate(num_posts=Count('id'))
    return {
        'date_list': date_list

    }

#分类模板标签
@register.inclusion_tag('blog/inclusions/_categories.html', takes_context=True)
def show_categories(context):
    category_list = Category.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)
    return {
        'category_list': category_list
    }

#标签云模板标签
@register.inclusion_tag('blog/inclusions/_tags.html',takes_context=True)
def show_tags(context):
    tag_list = Tag.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)
    return {
        'tag_list': tag_list
    }