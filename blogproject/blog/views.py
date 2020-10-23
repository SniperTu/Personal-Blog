# Create your views here.
from django.shortcuts import render, get_object_or_404
from .models import Post, Category, Tag
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension
import markdown
import re

def index(request):
    #-created_time中-号表示逆序，如果不加 - 则是正序
    post_list = Post.objects.all().order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list':post_list})
def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    # post.body = markdown.markdown(post.body,
    #                               extensions=[
    #                                   'markdown.extensions.extra',
    #                                   'markdown.extensions.codehilite',
    #                                   'markdown.extensions.toc',
    #                                   #在书写 Markdown 文本时，在你想生成目录的地方插入 [TOC] 标记即可
    #                               ])
    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',
        TocExtension(slugify=slugify),#添加标题锚点
    ])
    post.body = md.convert(post.body)
    m = re.search(r'<div class="toc">\s*<ul>\s*</div>', md.toc, re.S)
    post.toc = m.group(1) if m is not None else ''
    #post.toc = md.toc
    #先实例化了一个markdown.markdown()方法的对象md，也传入了extensions参数，
    # 使用实例的convert方法将post.body的markdown文本解析成HTML
    #这里的toc属性为动态属性，本身post是没有该属性的
    return render(request, 'blog/detail.html', context={'post': post})
def archive(request, year, month):
    post_list = Post.objects.filter(created_time__year=year,
                                    created_time__month=month).order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})

def category(request, pk):
    cate = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(category=cate).order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})

def tag(request, pk):
    t = get_object_or_404(Tag, pk=pk)
    post_list = Post.objects.filter(tags=t).order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})