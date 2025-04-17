from django.db import models
from accounts.models import Trainer
from django.contrib.auth import get_user_model

User = get_user_model()


VIDEO_CATEGORIES = [
    ('workout', 'Workout'),
    ('yoga', 'Yoga'),
    ('football', 'Football'),
    ('cricket', 'Cricket'),
    ('stretching', 'Stretching'),
    ('boxing', 'Boxing'),
    ('other', 'Other'),
]

FITNESS_LEVELS = [
    ('beginner', 'Beginner'),
    ('intermediate', 'Intermediate'),
    ('advanced', 'Advanced'),
]
# Course Model
class VideoCourse(models.Model):
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=255,choices=VIDEO_CATEGORIES)
    fitness_level = models.CharField(max_length=255,choices=FITNESS_LEVELS)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    thumbnail = models.ImageField(upload_to='course_thumbnails/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

# Individual Videos inside a Course
class CourseVideo(models.Model):
    course = models.ForeignKey(VideoCourse, on_delete=models.CASCADE, related_name='videos')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    thumbnail = models.ImageField(upload_to='video_thumbnails/', blank=True, null=True)
    video_file = models.FileField(upload_to='course_videos/')
    duration = models.DurationField()
    sequence = models.PositiveIntegerField()  # Determines order
    uploaded_at = models.DateTimeField(auto_now_add=True)

# Purchase Model
class CoursePurchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(VideoCourse, on_delete=models.CASCADE)
    purchased_at = models.DateTimeField(auto_now_add=True)

