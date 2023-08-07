from django.contrib import admin
from .models import Question  # 현재 디렉토리에서 Question import


# Register your models here.
class QuestionAdmin(admin.ModelAdmin):
    search_fields = ['subject']  # 제목으로 검색


admin.site.register(Question, QuestionAdmin)
