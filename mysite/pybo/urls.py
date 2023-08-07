from django.urls import path
from . import views  # 현재 디렉토리 내의 views

app_name = 'pybo'  # namespace

urlpatterns = [
    path('', views.index, name='index'),
    # /pybo/3
    path('<int:question_id>/', views.detail, name='detail'),

    # /pybo/answer/create/2
    path('answer/create/<int:question_id>', views.answer_create, name='answer_create'),

    # pybo:question_create
    path('question/create/', views.question_create, name='question_create'),

    # bootstrap : 디자인 템플릿 -> 목록
    path('boot/list/', views.boot_list, name='boot_list'),

    # bootstrap : 디자인 템플릿 -> 등록
    path('boot/reg/', views.boot_reg, name='boot_reg')
]
