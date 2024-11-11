from django.db import models
from django.utils import timezone
from datetime import timedelta
from accounts.models import GymUser, Trainer,GymOwner

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
