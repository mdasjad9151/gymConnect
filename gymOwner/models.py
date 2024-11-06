from django.db import models
from django.utils import timezone
from datetime import timedelta
from accounts.models import GymUser, Trainer,GymOwner

class TrainerRequest(models.Model):
    gym = models.ForeignKey(GymOwner, on_delete=models.CASCADE)
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, default="NA")
    request_date = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return self.request_date < timezone.now() - timedelta(minutes=2)
