from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone

from board.forms import AnswerForm
from board.models import Question, Answer


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
