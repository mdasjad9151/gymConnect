from django.db import models
from django.contrib.auth import get_user_model
import uuid
from gymOwner.models import Gym
from accounts.models import GymOwner

User = get_user_model()



class Membership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE)
    token_code = models.CharField(max_length=10, unique=True, default=uuid.uuid4)
    paid = models.BooleanField(default=False)
    start_date = models.DateField()
    expire_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.gym.name} ({self.start_date} to {self.expire_date})"
