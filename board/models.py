from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Question(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_question')
    subject = models.CharField(max_length=100)      #질문 제목
    content = models.TextField()                    #질문 내용
    create_date = models.DateTimeField()            #질문 작성일
    modify_date = models.DateTimeField(null=True, blank=True)            #질문 수정일
    voter = models.ManyToManyField(User, related_name='voter_question')            #추천수

    def __str__(self):
        return self.subject

class Answer(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_answer')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)    #외래키, 질문 제목
    content = models.TextField()                                        #답변 내용
    create_date = models.DateTimeField()                                #답변 작성일
    modify_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_answer')

    def __str__(self):
        return self.content

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)      #댓글 글쓴이
    content = models.TextField()                                    #댓글 내용
    create_date = models.DateTimeField()                            #작성일
    modify_date = models.DateTimeField(null=True, blank=True)       #수정일
    question = models.ForeignKey(Question, null=True, blank=True, on_delete=models.CASCADE)     #질문
    answer = models.ForeignKey(Answer, null=True, blank=True, on_delete=models.CASCADE)         #답변