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
    path('join_community', login_required(views.join_community), name='join_community'),
    path('edit_profile', login_required(views.edit_profile), name='edit_profile'),
    path('user_profile', login_required(views.display_user_profile), name='user_profile'),
    path('create_template', login_required(views.create_template), name='create_template'),
    path('search_communities/', login_required(views.search_communities), name='search_communities'),
    path('display_post/', login_required(views.display_post), name='display_post'),
    path('search_posts/', login_required(views.search_posts), name='search_posts'),
    path('edit_community/', login_required(views.edit_community), name='edit_community'),
    path('advanced_search_post', login_required(views.advanced_search_post), name='advanced_search_post'),
    path('get_template_dict', login_required(views.get_template_dict), name='get_template_dict'),
]