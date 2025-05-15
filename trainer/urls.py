from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('', views.trainer_dashboard, name='trainer_dashboard'),
    path('trainer-requests/', views.trainer_requests, name='trainer_requests'),

    # path('requests/', views.trainer_requests, name='requests_list'),
    path('requests/update/<int:request_id>/<str:action>/', views.update_request_status, name='update_request_status'),

    path('trainer-add-plans/', views.trainer_add_plans, name='trainer_add_plans'),
    path('get-user-plan/<int:user_id>/', views.get_user_plan, name='get_user_plan'),
    path('update-plan/', views.update_plan, name='update_plan'),


    path('gym/<int:gym_id>/', views.get_gym_list, name='get_gym_list'),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)