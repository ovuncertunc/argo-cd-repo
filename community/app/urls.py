from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', views.login_user, name='login_user'),
    path('login_user', views.login_user, name='login_user'),
    path('register', views.register, name='register'),
    path('home', login_required(views.home), name='home'),
    path('logout_user', views.logout_user, name='logout_user'),
    path('create_community', login_required(views.create_community), name='create_community'),
    path('community_home', login_required(views.community_home), name='community_home'),
    path('my_communities', login_required(views.my_communities), name='my_communities'),
    path('create_post', login_required(views.create_post), name='create_post'),
    path('join_community', login_required(views.join_community), name='join_community')
]