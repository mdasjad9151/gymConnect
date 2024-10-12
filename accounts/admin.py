from django.contrib import admin
from .models import Admin,GymOwner,Trainer,GymUser, BaseUser
# Register your models here.

admin.site.register(Admin)
admin.site.register(GymOwner)
admin.site.register(Trainer)
admin.site.register(GymUser)
admin.site.register(BaseUser)