from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_user, name='login_user'),
    path('login_user', views.login_user, name='login_user'),
    path('register', views.register, name='register'),
    path('home', views.home, name='home'),
    path('logout_user', views.logout_user, name='logout_user')
]