from django.urls import path
from board.views import base_views, question_views, answer_views, vote_views, comment_views

app_name = 'board'

urlpatterns = [
    #127.0.0.1:8000/board/ 라고 쳤을 때 views의 index로 들어감
    path('', base_views.index, name='index'),                                    #질문 목록
    path('boardlist', base_views.boardlist, name='boardlist'),                                    #질문 목록
    path('<int:question_id>/', base_views.detail, name='detail'),                #질문/답변 상세

    path('question/create/', question_views.question_create, name ='question_create'),               #질문 등록
    path ('question/modify/<int:question_id>/', question_views.question_modify, name='question_modify'),  #질문 삭제
    path ('question/delete/<int:question_id>/', question_views.question_delete, name='question_delete'),

    path('answer/create/<int:question_id>/', answer_views.answer_create, name='answer_create'),
    path ('answer/modify/<int:answer_id>/', answer_views.answer_modify, name='answer_modify'),
    path ('answer/delete/<int:answer_id>/', answer_views.answer_delete, name='answer_delete'),

    path ('comment/create/question/<int:question_id>/', comment_views.comment_create_question, name='comment_create_question'),
    path ('comment/modify/question/<int:comment_id>/', comment_views.comment_modify_question, name='comment_modify_question'),
    path ('comment/delete/question/<int:comment_id>/', comment_views.comment_delete_question, name='comment_delete_question'),

    path ('comment/create/answer/<int:answer_id>/', comment_views.comment_create_answer, name='comment_create_answer'),
    path ('comment/modify/answer/<int:comment_id>/', comment_views.comment_modify_answer, name='comment_modify_answer'),
    path ('comment/delete/answer/<int:comment_id>/', comment_views.comment_delete_answer, name='comment_delete_answer'),

    path ('vote/question/<int:question_id>/', vote_views.vote, name='vote'),
    path ('vote/answer/<int:answer_id>/', vote_views.vote, name='vote'),

]