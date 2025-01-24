from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User


class UserRegistrationForm(UserCreationForm):

    phone = forms.CharField(
        max_length=11,
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-control"}
        ),  # Bootstrap 스타일 적용
    )

    class Meta:
        model = User
        fields = ["username", "email", "phone", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Bootstrap 스타일 적용
        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control"


class LoginForm(
    AuthenticationForm
):  # AuthenticationForm은 기본적으로 제공되는 로그인 폼
    """로그인 폼"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Bootstrap 스타일 적용
        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control"


class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ["email", "phone"]
        widgets = {
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
        }
