from django import forms
from .models import Topic, Post


class NewTopicForm(forms.ModelForm):
    """
        这是我们的第⼀个 form。它是⼀个与 Topic model 相关联的
    ModelForm 。Meta 类⾥⾯ fields 列表中的 subject 引⽤ Topic 类中
    的 subject field(字段)。现在注意到我们定义了⼀个叫做 message 的额外
    字段。它⽤来引⽤ Post 中我们想要保存的 message。
    """
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 5, 'placeholder': '写点什么吧?， 现在支持markdown了！'}
        ),
        max_length=4000,
        help_text='内容最大长度4000')

    class Meta:
        model = Topic
        fields = ['subject', 'message']


class PostForm(forms.ModelForm):
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={'placeholder': '内容支持markdown哦！'}
        )
    )

    class Meta:
        model = Post
        fields = ['message', ]
