from django.shortcuts import render
from poll.models import Question, Choice


def index(request):
    poll_list = Question.objects.all()
    context = {'poll_list': poll_list}

    return render(request, 'poll/poll_list.html', context)

def detail(request, pk):
    question = Question.objects.get(id=pk)
    return render(request, 'poll/detail.html',{'question': question})

def vote(request, pk):
    question = Question.objects.get(id=pk)
    try:
        sel_choice = question.choice_set.get(id=request.POST['choice'])
    except KeyError:
        return render(request, 'poll/detail.html', {'question': question, 'error': '선택을 확인하세요'})
    else:
        sel_choice.votes = sel_choice.votes + 1
        sel_choice.save()
        return render(request, 'poll/result.html', {'question': question})