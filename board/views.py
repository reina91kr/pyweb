from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from board.models import Question, Answer, Comment
from board.forms import QuestionForm, AnswerForm, CommentForm
from django.contrib import messages


# Create your views here.

def index(request):
    #question_list = Question.objects.all()
    question_list = Question.objects.order_by('-create_date')

    #페이지 처리
    page = request.GET.get('page', 1)       #127.0.0.1:8000/  - 1페이지
    paginator = Paginator(question_list, 10)
    page_obj = paginator.get_page(page)  # 페이지 가져오기

    return render(request, 'board/question_list.html', {'question_list':page_obj})

def detail(request, question_id):
    #question = Question.objects.get(id=question_id)
    question = get_object_or_404(Question, pk = question_id)
    #결과에 오류가 있을 때 404 처리
    return render(request, 'board/detail.html', {'question':question})

@login_required(login_url='common:login')
def question_create(request):
    #질문 등록
    if request.method == 'POST':
        form = QuestionForm(request.POST)       #자료 수집
        if form.is_valid():
            question = form.save(commit=False)      #가저장 (날짜가 없음)
            question.create_date = timezone.now()      #날짜 추가등록
            question.author = request.user
            question.save()         #질문 등록하기 (최종적으로 저장하기) = q.save()
            return redirect ('board:index')     #이동할 경로 (앱 네임사용) 저장
    else:
        form = QuestionForm()       #폼 객체 생성
    return render(request, 'board/question_form.html', {'form':form})

@login_required(login_url='common:login')
def answer_create(request, question_id):
    question = Question.objects.get(id=question_id)     #해당 ID의 질문 객체 생성
    if request.method == "POST":
        form = AnswerForm(request.POST)     #입력값 전달받음
        if form.is_valid():             #입력이 모두 되었다면 (유효성 검사)
            answer = form.save(commit=False)        #내용 저장
            answer.create_date = timezone.now()     #작성일 저장
            answer.author = request.user
            answer.question = question              #외래키 저장 (model의 answer의 question을 여기의 question으로 저장)
            answer.save()
            return redirect('board:detail', question_id=question.id)
    else:                                       #입력이 안된 경우 (유효성 검사)
        form = AnswerForm()
    return render(request, 'board/detail.html', {'form':form, 'question':question})

@login_required(login_url='common:login')
def question_modify(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.modify_date = timezone.now()
            question.save()
            return redirect('board:detail', question_id=question.id)
    else:
        form = QuestionForm(instance=question) #instance: 폼에 내용이 채워짐
    return render(request, 'board/question_form.html', {'form':form})

@login_required(login_url='common:login')
def answer_modify(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.method == "POST":
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.modify_date = timezone.now()
            answer.save()
            return redirect('board:detail', question_id=answer.question.id)
    else:
        form = AnswerForm(instance=answer)
    return render(request, 'board/answer_form.html', {'answer':answer, 'form':form})

@login_required(login_url='common:login')
def answer_delete(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    answer.delete()
    return redirect ('board:detail', question_id=answer.question.id)

@login_required(login_url='common:login')
def question_delete(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    question.delete()  #질문 삭제
    return redirect('board:index')

@login_required(login_url='common:login')
def comment_create_question(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.create_date = timezone.now()
            comment.question = question
            comment.save()
            return redirect('board:detail', question_id=question.id)
    else:
        form = CommentForm()
    return render(request, 'board/comment_form.html', {'form':form})

@login_required(login_url='common:login')
def comment_modify_question(request, comment_id):
    comment=get_object_or_404(Comment, pk=comment_id)
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.modify_date = timezone.now()
            comment.save()
            return redirect('board:detail', question_id = comment.question.id)
    else:
        form = CommentForm(instance=comment)
        return render(request, 'board/comment_form.html', {'form': form})

@login_required(login_url='common:login')
def comment_delete_question(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    comment.delete()
    return redirect ('board:detail', question_id=comment.question_id)

@login_required(login_url='common:login')
def comment_create_answer(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.create_date = timezone.now()
            comment.answer = answer
            comment.save()
            return redirect('board:detail', question_id=comment.answer.question.id)
    else:
        form = CommentForm()
    return render(request, 'board/comment_form.html', {'form':form})

@login_required(login_url='common:login')
def comment_modify_answer(request, comment_id):
    comment=get_object_or_404(Comment, pk=comment_id)
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.modify_date = timezone.now()
            comment.save()
            return redirect('board:detail', question_id = comment.answer.question.id)
    else:
        form = CommentForm(instance=comment)
    return render(request, 'board/comment_form.html', {'form': form})

@login_required(login_url='common:login')
def comment_delete_answer(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    comment.delete()
    return redirect ('board:detail', question_id=comment.answer.question_id)