from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from ..forms import QuestionForm
from ..models import Question

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
def question_delete(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    question.delete()  #질문 삭제
    return redirect('board:index')

