from django.contrib import admin

from .models import VideoCourse,CourseVideo,CoursePurchase
# Register your models here.

admin.site.register(VideoCourse)
admin.site.register(CourseVideo)
admin.site.register(CoursePurchase)