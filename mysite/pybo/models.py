from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Question(models.Model):
    subject = models.CharField(max_length=200)  # 가변형 문자열
    content = models.TextField()  # CLOB, 글자 수 제한이 없는 textfield
    create_date = models.DateTimeField()  # 날짜 + 시간

    """model author 추가"""
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.subject


class Answer(models.Model):
    # Question이 삭제될 경우 Answer도 같이 삭제
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()

    """model author 추가"""
    author = models.ForeignKey(User, on_delete=models.CASCADE)
