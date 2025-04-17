from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import (
    register_admin, register_gym_owner, register_trainer, register_gym_user, 
    user_login, user_logout, dashboard
)

app_name = 'accounts'
urlpatterns = [
    path('register/admin/', register_admin, name='register_admin'),
    path('register/gym-owner/', register_gym_owner, name='register_gym_owner'),
    path('register/trainer/', register_trainer, name='register_trainer'),
    path('register/gym-user/', register_gym_user, name='register_gym_user'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.create_admin, name = 'superuser'),
# ]