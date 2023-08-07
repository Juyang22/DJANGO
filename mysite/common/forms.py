from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from pybo.pcwk_logging import logger2 as plog


# UserCreationForm : username(사용자 이름), password1(비밀번호), password2(비밀번호 확인)
class UserForm(UserCreationForm):
    email = forms.EmailField(label='이메일')  # email 속성 추가

    class Meta:
        model = User
        fields = ('username', 'email')
