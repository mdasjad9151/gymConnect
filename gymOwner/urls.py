from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views  # Assuming your views are in the 'core' app

urlpatterns = [
    path('dashboard-gym/', views.gym_owner_deshboard, name='gym_owner_deshboard'),

    path('assign-user/', views.assign_user, name='assign_trainer'),

    path('add-trainer/', views.add_trainer, name='add_trainer'),
    path('get-trainer-details/<int:trainer_id>/', views.get_trainer_details, name='get_trainer_details'),
    path('create-trainer-request/', views.create_trainer_request, name='create-trainer-request'),

    
    path('list-users/', views.list_users, name='list_users'),
    path('list-trainers/', views.list_trainers, name='list_trainers'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
