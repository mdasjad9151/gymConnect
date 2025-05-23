from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('create/', views.create_post, name='create_post'),
    path('like/<int:post_id>/', views.like_post, name='like_post'),
    path('comment/add/<int:post_id>/', views.add_comment, name='add_comment'),
    path('comment/load/<int:post_id>/', views.load_comments, name='load_comments'),
    path('follow/<int:user_id>/', views.follow_user, name='follow_user'),
]
