from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import VideoCourse, CourseVideo, CoursePurchase
from .forms import VideoCourseForm, CourseVideoForm
import subprocess
from django.http import StreamingHttpResponse
import os
from django.conf import settings
from accounts.decorators import trainer_required
# Trainer: Create a new course
@trainer_required
def create_course(request):
    if request.method == 'POST':
        form = VideoCourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.trainer = request.user.trainer  # Assuming trainer is linked to user
            course.save()
            return redirect('trainer_courses')
    else:
        form = VideoCourseForm()
    return render(request, 'course/create_course.html', {'form': form})


# Trainer: Add video to a course
@login_required
def add_course_video(request, course_id):
    course = get_object_or_404(VideoCourse, id=course_id, trainer=request.user.trainer)
    if request.method == 'POST':
        form = CourseVideoForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            video.course = course
            video.save()
            return redirect('trainer_courses')
    else:
        form = CourseVideoForm()
    return render(request, 'course/add_video.html', {'form': form, 'course': course})


# Trainer: List own courses
@login_required
def trainer_courses(request):
    courses = VideoCourse.objects.filter(trainer=request.user.trainer).prefetch_related('videos')
    return render(request, 'course/trainer_courses.html', {'courses': courses})


# User: List all available courses
from collections import defaultdict





def course_list(request):
    courses_by_category = defaultdict(list)
    
    for course in VideoCourse.objects.all():
        category_name = course.get_category_display()  # Get the display label from choices
        courses_by_category[category_name].append(course)

    return render(request, 'course/course_list.html', {
        'courses_by_category': dict(courses_by_category)
    })




# User: View course details
@login_required
def course_detail(request, course_id):
    course = get_object_or_404(VideoCourse, id=course_id)
    videos = course.videos.order_by('sequence')
    is_purchased = False
    if request.user.is_authenticated:
        is_purchased = CoursePurchase.objects.filter(user=request.user, course=course).exists()
    return render(request, 'course/course_detail.html', {
        'course': course,
        'videos': videos,
        'is_purchased': is_purchased
    })


# User: Purchase course
@login_required
def purchase_course(request, course_id):
    course = get_object_or_404(VideoCourse, id=course_id)
    CoursePurchase.objects.get_or_create(user=request.user, course=course)
    return redirect('course_detail', course_id=course.id)


# User: View purchased courses
@login_required
def my_courses(request):
    purchases = CoursePurchase.objects.filter(user=request.user).select_related('course')
    return render(request, 'course/my_courses.html', {'purchases': purchases})

@login_required
def course_videos(request, course_id):
    course = get_object_or_404(VideoCourse, id=course_id)
    # Ensure user purchased this course
    if not CoursePurchase.objects.filter(user=request.user, course=course).exists():
        return redirect('my_courses')

    videos = course.videos.order_by('sequence')
    print(videos)
    return render(request, 'course/course_videos.html', {
        'course': course,
        'videos': videos
    })

def watch_video(request, video_id):
    video = get_object_or_404(CourseVideo, id=video_id)
    return render(request, 'course/watch_video.html', {'video_id': video_id, 'duration': video.duration })
