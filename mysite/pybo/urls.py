from django.urls import path
from . import views  # 현재 디렉토리 내의 views

app_name = 'pybo'  # namespace

urlpatterns = [
    path('', views.index, name='index'),
    # /pybo/3
    path('<int:question_id>/', views.detail, name='detail'),

    # pybo:question_create
    path('question/create/', views.question_create, name='question_create'),

    # /pybo/answer/create/2
    path('answer/create/<int:question_id>', views.answer_create, name='answer_create'),

    # question_modify
    path('question/modify/<int:question_id>', views.question_modify, name='question_modify'),

    # question_delete
    path('question/delete/<int:question_id>', views.question_delete, name='question_delete'),

    # answer_modify
    path('answer/modify/<int:answer_id>', views.answer_modify, name='answer_modify'),

    # answer_delete
    path('question/delete/<int:answer_id>', views.answer_delete, name='answer_delete'),

    # bootstrap : 디자인 템플릿 -> 목록
    path('boot/list/', views.boot_list, name='boot_list'),

    # bootstrap : 디자인 템플릿 -> 등록
    path('boot/reg/', views.boot_reg, name='boot_reg')

]
