from django.db import models
from accounts.models import GymUser
# Create your models here.
class Plan(models.Model):
    user = models.ForeignKey(GymUser, on_delete=models.CASCADE)
    workout = models.TextField()
    diet = models.TextField()
    update_date = models.DateTimeField(auto_now=True, blank=True)