from django.db import models
from django.contrib.auth.models import  User
from django.urls import  reverse
from django.utils import timezone
import  markdown,re
from django.utils.html import strip_tags
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension
from django.utils.functional import cached_property
# Create your models here.

#分类表
class Category(models.Model):
    name = models.CharField(max_length=100)
    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name

#标签
class Tag(models.Model):
    name = models.CharField(max_length=100)
    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name

#文章
class Post(models.Model):
    title = models.CharField('标题', max_length=70)
    body = models.TextField('正文')
    create_time = models.DateTimeField('创建时间')
    modified_time = models.DateTimeField('修改时间')
    excerpt = models.CharField('摘要', max_length=200, blank=True) # blank=True  表示可以为空
    category = models.ForeignKey(Category,verbose_name='分类', on_delete=models.CASCADE)
    tags = models.ForeignKey(Tag,verbose_name='标签', blank=True, on_delete=models.CASCADE,default=1)
    author = models.ForeignKey(User,verbose_name='作者', on_delete=models.CASCADE) # CASCADE :级别删除
    views = models.PositiveIntegerField(default=0,editable=False)
    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ['-create_time','title']
    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk':self.pk})
    def save(self,*args,**kwargs):
        self.modified_time = timezone.now()
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
        ])
        self.excerpt = strip_tags(md.convert(self.body))[:54]
        super().save(*args,**kwargs)
    def increase_views(self):
        self.views +=1
        self.save(update_fields=['views'])
    @property
    def toc(self):
        return self.rich_content.get("toc","")
    @property
    def body_html(self):
        return self.rich_content.get("content","")
    @cached_property
    def rich_content(self):
        return generate_rich_content(self.body)

def generate_rich_content(value):
    md = markdown.Markdown(
        extensions = [
            "markdown.extensions.extra",
            "markdown.extensions.codehilite",
            TocExtension(slugify=slugify),
        ]
    )
    content = md.convert(value)
    m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
    toc = m.group(1) if m is not None else ""
    return {"content": content, "toc": toc}