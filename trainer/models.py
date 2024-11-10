from django.db import models
from accounts.models import GymUser

class Plan(models.Model):
    user = models.ForeignKey(GymUser, on_delete=models.CASCADE)

    # Workout fields for each day of the week
    monday_workout = models.TextField(blank=True)
    tuesday_workout = models.TextField(blank=True)
    wednesday_workout = models.TextField(blank=True)
    thursday_workout = models.TextField(blank=True)
    friday_workout = models.TextField(blank=True)
    saturday_workout = models.TextField(blank=True)

    # Diet fields with breakdown for each meal
    breakfast = models.TextField(blank=True)
    lunch = models.TextField(blank=True)
    dinner = models.TextField(blank=True)
    preworkout_diet = models.TextField(blank=True)

    # Automatically updates every time the model is saved
    update_date = models.DateTimeField(auto_now=True, blank=True)

    def __str__(self):
        return f"Workout Plan for {self.user}"
