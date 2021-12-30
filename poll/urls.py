import board.views as views
from django.urls import path
from board.views import vote_views

app_name = 'poll'

urlpatterns = [
    path('', vote_views.index, name='index'),
    path('<int:pk>/', vote_views.detail, name='detail'),
    path('<int:pk>/vote/', vote_views.vote, name='vote'),
]