from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

#views가 많기 때문에 auth_views라는 이름을 붙임


app_name = 'common'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(
        template_name='common/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
]