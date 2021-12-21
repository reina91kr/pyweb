from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from board.models import Question
from board.forms import QuestionForm, AnswerForm

# Create your views here.

def index(request):
    question_list = Question.objects.all()
    return render(request, 'board/question_list.html', {'question_list':question_list})

def detail(request, question_id):
    question = Question.objects.get(id=question_id)
    return render(request, 'board/detail.html', {'question':question})

def question_create(request):
    #질문 등록
    if request.method == 'POST':
        form = QuestionForm(request.POST)       #자료 수집
        if form.is_valid():
            question = form.save(commit=False)      #가저장 (날짜가 없음)
            question.create_date = timezone.now()      #날짜 추가등록
            question.save()         #질문 등록하기 (최종적으로 저장하기) = q.save()
            return redirect ('board:index')     #이동할 경로 (앱 네임사용) 저장
    else:
        form = QuestionForm()       #폼 객체 생성
    return render(request, 'board/question_form.html', {'form':form})

def answer_create(request, question_id):
    question = Question.objects.get(id=question_id)     #해당 ID의 질문 객체 생성
    if request.method == "POST":
        form = AnswerForm(request.POST)     #입력값 전달받음
        if form.is_valid():             #입력이 모두 되었다면 (유효성 검사)
            answer = form.save(commit=False)        #내용 저장
            answer.create_date = timezone.now()     #작성일 저장
            answer.question = question              #외래키 저장 (model의 answer의 question을 여기의 question으로 저장)
            answer.save()
            return redirect('board:detail', question_id=question.id)
    else:                                       #입력이 안된 경우 (유효성 검사)
        form = AnswerForm()
    return render(request, 'board/detail.html', {'form':form, 'question':question})

