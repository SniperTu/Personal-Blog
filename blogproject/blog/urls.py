#记录不同网址对应的处理函数，当用户访问某网站时，django会在本文件中找，
# 如果找到则调用和它绑在一起的处理函数（视图函数）
from django.urls import path
from . import views
#通过 app_name='blog' 告诉 django 这个 urls.py 模块是属于 blog 应用的
app_name = 'blog'
urlpatterns = [
    path('', views.index, name='index'),
    #django路由匹配规则的特殊写法，作用是从用户访问的url中把匹配到的数字捕获并作为关键字参数传给其对应的视图函数detail
    path('posts/<int:pk>/', views.detail, name='detail'),
    path('archives/<int:year>/<int:month>/',views.archive, name='archive'),
    path('categories/<int:pk>/', views.category, name='category'),
    path('tags/<int:pk>', views.tag, name='tag'),
]