from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator
from board.models import Question

def index(request):
    return render(request, 'board/index.html')

def boardlist(request):
    page = request.GET.get('page', 1)       #127.0.0.1:8000/  - 1페이지
    kw = request.GET.get('kw', '')      #검색어 가져오기

    question_list = Question.objects.order_by('-create_date')
    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |
            Q(content__icontains=kw) |
            Q(author__username__icontains=kw) |
            Q(answer__author__username__icontains=kw)|
            Q(answer__content__icontains=kw)
        ).distinct()

    paginator = Paginator(question_list, 10)
    page_obj = paginator.get_page(page)  # 페이지 가져오기

    return render(request, 'board/question_list.html', {'question_list':page_obj, 'page':page, 'kw':kw})

def detail(request, question_id):
    #question = Question.objects.get(id=question_id)
    question = get_object_or_404(Question, pk = question_id)
    #결과에 오류가 있을 때 404 처리
    return render(request, 'board/detail.html', {'question':question})

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect

from board.models import Answer
from board.models import Question


@login_required(login_url='common:login')
def vote_question(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user == question.author:
        messages.error(request, '본인이 작성한 글은 추천할 수 없습니다')
    else:
        question.voter.add(request.user)
    return redirect('board:detail', question_id=question.id)

@login_required(login_url='common:login')
def vote_answer(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user == answer.author:
        messages.error(request, '본인이 작성한 글은 추천할 수 없습니다')
    else:
        answer.voter.add(request.user)
    return redirect('board:detail', question_id=answer.question.id)
