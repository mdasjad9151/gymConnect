from django.db import models
from django.utils import timezone
from datetime import timedelta
from accounts.models import GymUser, Trainer,GymOwner
from django.contrib.auth import get_user_model
import uuid


User = get_user_model()


class TrainerRequest(models.Model):
    gym = models.ForeignKey(GymOwner, on_delete=models.CASCADE)
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]
    
    request_data = models.TextField(blank=True, null=True)  # Example field for request data.
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    request_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.gym.gym_name)+" - "+ self.trainer.name

class Gym(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length =100, blank= True)
    pincode = models.PositiveIntegerField(blank=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    price_per_day = models.DecimalField(max_digits=6, decimal_places=2)

    gym_logo = models.ImageField(upload_to= 'gym_logo/', blank = True)
    average_rating = models.FloatField(default=0.0, blank=True)
    rating_count = models.PositiveIntegerField(default=0, blank= True)

    def __str__(self):
        return self.name


class GymImage(models.Model):
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='gym_images/')


    def __str__(self):
        return  self.gym.name


class GymRating(models.Model):
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()  # Example: 1 to 5 stars
    review = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('gym', 'user')  # Prevent duplicate ratings

    def __str__(self):
        return f"{self.user.username} rated {self.gym.name}: {self.rating}"
