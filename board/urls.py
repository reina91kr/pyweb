from django.urls import path
from board import views

app_name = 'board'

urlpatterns = [
    #127.0.0.1:8000/board/ 라고 쳤을 때 views의 index로 들어감
    path('', views.index, name='index'),                                    #질문 목록
    path('<int:question_id>/', views.detail, name='detail'),                #질문/답변 상세
    path('question/create/', views.question_create, name ='question_create'),               #질문 등록
    path('answer/create/<int:question_id>', views.answer_create, name='answer_create'),                    #답변 등록

]