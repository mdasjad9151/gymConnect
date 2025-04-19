from django.contrib import admin
from .models import TrainerRequest, Gym, GymImage
# Register your models here.
admin.site.register(TrainerRequest)
admin.site.register(Gym)
admin.site.register(GymImage)