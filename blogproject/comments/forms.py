from django import forms
from .models import Comment

# django 的表单类必须继承自 forms.Form 类或者 forms.ModelForm 类
#django 会根据表单类的定义自动生成表单的 HTML 代码，
# 我们要做的就是实例化这个表单类，然后将表单的实例传给模板，让 django 的模板引擎来渲染这个表单。
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'url', 'text']
