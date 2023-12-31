from django.http import HttpResponse
from .models import Question, Answer
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .forms import QuestionForm, AnswerForm

import logging
logger = logging.getLogger(__name__)

# logger2
from .pcwk_logging import logger2 as plog
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required  # 로그인 필수 처리
from django.contrib import messages  # 강제로 예외 발생


# Create your views here.
# http://127.0.0.1:8000/pybo
@login_required(login_url='common:login')
def answer_delete(request, answer_id):
    """
    답변 삭제
    """
    plog.debug('answer_id : {}'.format(answer_id))

    # 기존 answer 데이터 읽기
    answer = get_object_or_404(Answer, pk=answer_id)
    plog.debug('answer : {}'.format(answer))

    # 권한 Check: 답변 단 사람만 삭제 가능
    if request.user != answer.author:
        messages.error(request, '삭제 권한이 없습니다.')
    else:
        answer.delete()

    return redirect('pybo:detail', question_id=answer.question.id)


@login_required(login_url='common:login')
def answer_modify(request, answer_id):
    """
    답변 수정
    """
    plog.debug('answer_id : {}'.format(answer_id))

    # 기존 answer 데이터 읽기
    answer = get_object_or_404(Answer, pk=answer_id)
    plog.debug('answer : {}'.format(answer))

    if request.user != answer.author:
        messages.error(request, '수정 권한이 없습니다.')
        return redirect('pybo:detail', question_id=answer.question.id)

    if request.method == 'POST':  # 수정 실행
        form = AnswerForm(request.POST, instance=answer)

        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.modify_date = timezone.now()
            answer.save()
            return redirect('pybo:detail', question_id=answer.question.id)

    else:  # 수정 form
        form = AnswerForm(instance=answer)

    context = {'answer': answer, 'form': form}
    return render(request, 'pybo/answer_form.html', context)


@login_required(login_url='common:login')
def question_delete(request, question_id):
    """
    질문 삭제
    """
    plog.debug('1. question_id : {}'.format(question_id))

    question = get_object_or_404(Question, pk=question_id)
    plog.debug('2. question : {}'.format(question))

    # 로그인한 사람과, 글쓴이가 서로 다르면 예외 발생
    if request.user != question.author:
        messages.error(request, '삭제 권한이 없습니다.')  # 예외 발생
        return redirect('pybo:detail', question_id=question_id)

    question.delete()
    return redirect('pybo:index')


@login_required(login_url='common:login')
def question_modify(request, question_id):
    """
    질문 수정
    """
    plog.debug('1. question_id : {}'.format(question_id))
    question = get_object_or_404(Question, pk=question_id)  # id=question_id 가능

    plog.debug('2. question : {}'.format(question))
    plog.debug('3. request.user : {}'.format(request.user))

    # 로그인한 사람과, 글쓴이가 서로 다르면 예외 발생
    if request.user != question.author:
        messages.error(request, '수정 권한이 없습니다.')  # 예외 발생
        return redirect('pybo:detail', question_id=question_id)

    if request.method == "POST":  # 수정
        form = QuestionForm(request.POST, instance=question)

        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.modify_date = timezone.now()  # 수정일시
            question.save()
            return redirect('pybo:detail', question_id=question_id)
    else:
        form = QuestionForm(instance=question)  # 데이터가 들어있는 form 생성
    context = {'form': form}

    return render(request, 'pybo/question_form.html', context)


def boot_reg(request):
    """ 개발에 사용될 bootstrap 등록 템플릿 """
    return render(request, 'pybo/reg.html')


def boot_list(request):
    """ 개발에 사용될 bootstrap 목록 템플릿 """
    return render(request, 'pybo/list.html')


@login_required(login_url='common:login')
def question_create(request):
    """
    질문 등록 : POST 요청이 들어오면 저장, 그렇지 않으면(GET) 화면 생성
    2023-08-07 : 질문 등록자 추가
    """
    plog.debug('1. request.method : {}'.format(request.method))

    if request.method == 'POST':
        form = QuestionForm(request.POST)

        if form.is_valid():  # form 유효하지 않으면 화면으로 메시지 전달
            question = form.save(commit=False)  # 임시 저장

            # author 추가
            question.author = request.user
            plog.debug("request.user : {}".format(request.user))
            question.create_date = timezone.now()  # 질문 등록일 저장
            question.save()  # 최종 저장
            return redirect('pybo:index')  # http://127.0.0.1:8000/pybo/

    else:
        form = QuestionForm()
    context = {'form': form}

    # QuestionForm을 pybo/question_form.html에 전달
    return render(request, 'pybo/question_form.html', {'form': form})


def index(request):
    """
    pybo 질문 목록
    """

    # get page
    page = request.GET.get('page', '1')  # 1은 default 값

    plog.debug('page : {}'.format(page))

    # Question.objects.order_by('create_date')  # order by create_date asc
    question_list = Question.objects.order_by('-create_date')  # order by create_date desc

    #
    paginator = Paginator(question_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    plog.debug('page_obj: {}'.format(page_obj))

    context = {'question_list': page_obj}  # 데이터를 딕셔너리로 저장

    # {% 장고 코드 추가 %}
    # question_list.html 템플릿 -> django 태그를 추가로 사용 가능(cf. jsp)
    return render(request, 'pybo/question_list.html', context)


def detail(request, question_id):
    """
    상세 조회: 단건 조회
    """
    plog.debug('1. question_id : {}'.format(question_id))
    # question = Question.objects.get(id=question_id)
    question = get_object_or_404(Question, id=question_id)

    plog.debug('2. question : {}'.format(question))
    context = {'question': question}  # 데이터를 딕셔너리로 저장

    # request, 템플릿 파일, 데이터(딕셔너리)
    return render(request, 'pybo/question_detail.html', context)


@login_required(login_url='common:login')
def answer_create(request, question_id):
    """
    답변 등록
    답변 등록자 추가 (2023-08-07)
    """
    # logger 사용
    plog.debug('1. answer_create question_id : {}'.format(question_id))

    question = get_object_or_404(Question, id=question_id)
    plog.debug('2. question: {}'.format(question))

    if request.method == 'POST':  # 등록
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            # author 추가
            answer.author      = request.user  # author 추가
            answer.create_date = timezone.now()  # 날짜 데이터
            answer.question    = question  # question_id
            answer.save()    # DB 저장
            return redirect('pybo:detail', question_id=question.id)

    else:                         # AnswerForm()
        form = AnswerForm()
    context = {'question': question, 'form': form}

    # 등록 이후 페이지 이동
    return render(request, 'pybo/question_detail.html', context)
