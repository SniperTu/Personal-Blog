import re

import markdown
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.html import strip_tags
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension

class Category(models.Model):
    """
    django要求模型必须继承models.Model类，
    Category只需要一个简单的分类名 name 就可以了，
    CharField指定了分类名name的数据类型，CharField是字符型，
    CharField的max_length参数指定其最大长度，超过这个长度的分类名就不能被存入数据库，
    """
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Tag(models.Model):
    """
    必须继承models.Model类
    """
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Post(models.Model):
    # 文章标题
    title = models.CharField('标题', max_length=70)
    # 文章正文使用TextField存储一大段文本
    body = models.TextField('正文')
    # 存储时间的字段用DateTimeField类型
    modified_time = models.DateTimeField('修改时间')
    created_time = models.DateTimeField('创建时间', default=timezone.now)
    # 文章摘要，可以没有文章摘要，但默认情况下CharField要求我们必须存入数据，否则会报错
    # 指定CharField的blank=True参数值就可以允许为空值了
    excerpt = models.CharField('摘要', max_length=200, blank=True)
    # 规定一篇文章只能对应一个分类，但是一个分类下可以有多篇文章，所以使用ForeignKey,即一对多的关联关系。
    # 自 django 2.0 以后，ForeignKey 必须传入一个 on_delete 参数用来指定当关联的
    # 数据被删除时，被关联的数据的行为，我们这里假定当某个分类被删除时，该分类下全部文章也同时被删除，因此     # 使用 models.CASCADE 参数，意为级联删除。
    # 而对于标签来说，一篇文章可以有多个标签，同一个标签下也可能有多篇文章，所以我们使用
    # ManyToManyField，表明这是多对多的关联关系。
    # 同时我们规定文章可以没有标签，因此为标签 tags 指定了 blank=True。
    category = models.ForeignKey(Category, verbose_name='分类', on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, verbose_name='标签', blank=True)
    # 文章作者，这里User是从django.contrib.auth.models导入的。
    # 通过ForeignKey把文章和User关联起来，一篇文章有一个作者，一个作者可以写多篇文章，和category类似
    author = models.ForeignKey(User, verbose_name='作者', on_delete=models.CASCADE)

    # 由于ForeignKey、ManyToManyField第一个参数必须传入其关联的Model，所以category、tags等字段需要使用参数verbose_name.

    def save(self, *args, **kwargs):
        self.modified_time = timezone.now()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ['-created_time']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})





