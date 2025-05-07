from django.contrib import admin

from .models import ConnectionRequest, PrivateMessage

admin.site.register(ConnectionRequest)
admin.site.register(PrivateMessage)
