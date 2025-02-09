from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Blog(models.Model):
    trainer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blogs')
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='likes')

    class Meta:
        unique_together = ('user', 'blog')  # Prevent duplicate likes

class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    trainer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')

    class Meta:
        unique_together = ('user', 'trainer')  # Prevent duplicate follows
