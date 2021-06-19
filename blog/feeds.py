# RSS 博客订阅

from django.contrib.syndication.views import Feed
from .models import Post

class AllPostsRssFeed(Feed):
    title = 'LYC-BLOG-tutorial'
    link = '/'
    describtion = 'LYC-BLOG-tutorial 所有文章'
    def items(self):
        return Post.objects.all()

    def items_title(self,item):
        return "[%s] %s" % (item.category, item.title)

    def item_description(self,item):
        return item.body_html
