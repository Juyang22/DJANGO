from django.urls import path
from . import views  # 현재 디렉토리 내의 views
from django.contrib.auth import views as auth_views

app_name = 'common'  # namespace

urlpatterns = [
    # django.contrib.auth 앱의 LoginView 클래스를 활용했으므로
    # 별도의 views.py 파일 불필요!
    path('login/', auth_views.LoginView.as_view(template_name='common/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # 회원가입
    path('signup/', views.signup, name='signup')
]
