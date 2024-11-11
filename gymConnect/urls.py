
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),  # Home page URL
    path('accounts/', include("accounts.urls")), #account urls 
    path('gym-owner/', include("gymOwner.urls")), #gym owner urls 
    path('gym-trainer/', include("trainer.urls")), #trainer urls 
    path('gym-user/', include("gymUser.urls")), #trainer urls 

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
