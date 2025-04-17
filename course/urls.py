from django.urls import path
from . import views

urlpatterns = [
    # Trainer URLs
    path('trainer/create-course/', views.create_course, name='create_course'),
    path('trainer/courses/', views.trainer_courses, name='trainer_courses'),
    path('trainer/add-video/<int:course_id>/', views.add_course_video, name='add_course_video'),

    # User URLs
    path('courses/', views.course_list, name='course_list'),
    path('courses/<int:course_id>/', views.course_detail, name='course_detail'),
    path('courses/<int:course_id>/purchase/', views.purchase_course, name='purchase_course'),
    path('my-courses/', views.my_courses, name='my_courses'),
    path('my-courses/<int:course_id>/', views.course_videos, name='course_videos'),
  
    path('watch-video/<int:video_id>/', views.watch_video, name='watch_video'),
# path('stream-video/<int:video_id>/', views.stream_test, name='stream_video'),

]
