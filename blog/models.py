from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blogs')

    data = models.JSONField(null=True, blank=True)  # new merged field
    created_at = models.DateTimeField(auto_now_add=True)

    
    # def __str__(self):
        
    #     return self


class Blog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='temp_blogs')
    content = models.JSONField()  # Safe to use if Django >= 3.1 and not PostgreSQL
    image = models.ImageField(upload_to='Post/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')

    class Meta:
        unique_together = ('user', 'post')  # Prevent duplicate likes

class Follow(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')

    class Meta:
        unique_together = ('user1', 'user2')  # Prevent duplicate follows
