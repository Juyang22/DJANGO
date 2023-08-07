from django import forms
from pybo.models import Question, Answer


class AnswerForm(forms.ModelForm):
    class Meta:  # model, fields 속성을 정의
        model = Answer
        fields = ['content']

        labels = {
            'content': '답변 내용'
        }


class QuestionForm(forms.ModelForm):
    class Meta:  # model, fields 속성을 정의
        model = Question
        fields = ['subject', 'content']

        # 라벨 변경
        labels = {
            'subject': '제목',
            'content': '내용'
        }
