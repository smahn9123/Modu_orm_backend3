from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = "__all__"


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        # 유저로부터 입력받을 필드만 기입
        fields = ["message"]
