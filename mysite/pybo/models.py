from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Question(models.Model):
    subject = models.CharField(max_length=200)  # 가변형 문자열
    content = models.TextField()  # CLOB, 글자 수 제한이 없는 textfield
    create_date = models.DateTimeField()  # 날짜 + 시간

    """ model author 추가: user """
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    """ 수정 
    null=True : null값 허용
    blank=True : form.is_valid()로 form 검사 시 값이 없어도 pass
    """
    modify_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.subject


class Answer(models.Model):
    # Question이 삭제될 경우 Answer도 같이 삭제
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()

    """model author 추가"""
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    """ 수정 
        null=True : null값 허용
        blank=True : form.is_valid()로 form 검사 시 값이 없어도 pass
        """
    modify_date = models.DateTimeField(null=True, blank=True)


class Comment(models.Model):
    """
    댓글
    """
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()  # 글자 수 제한 X
    create_date = models.DateTimeField()  # 날짜 + 시간, 작성일
    # null = True : DB에 null 허용
    # blank = True : form.is_valid()에 form 검사 시 값이 없어도 OK
    modify_date = models.DateTimeField(null=True, blank=True)  # 수정일
    # 댓글이 달린 질문 ID
    question = models.ForeignKey(Question, null=True, blank=True, on_delete=models.CASCADE)
    # 댓글이 달린 답변 ID
    answer   = models.ForeignKey(Answer, null=True, blank=True, on_delete=models.CASCADE)
