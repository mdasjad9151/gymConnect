from django.urls import path
from . import views

urlpatterns = [
    path("create/", views.create_blog, name="create_blog"),
    path("edit/<int:blog_id>/", views.edit_blog, name="edit_blog"),
    path("delete/<int:blog_id>/", views.delete_blog, name="delete_blog"),
    path("<int:blog_id>/comment/", views.add_comment, name="add_comment"),
    path("<int:blog_id>/like/", views.like_blog, name="like_blog"),
    path("trainers/<int:trainer_id>/follow/", views.follow_trainer, name="follow_trainer"),
    path("post/", views.blog_list, name="blog_list"),
    path("<slug:slug>/", views.blog_detail, name="blog_detail"),
]
