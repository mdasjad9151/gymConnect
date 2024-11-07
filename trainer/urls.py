from django.urls import path
from . import views

urlpatterns = [
    path('', views.trainer_dashboard, name='trainer_dashboard'),
    path('trainer-requests/', views.trainer_requests, name='trainer_requests'),

    # path('requests/', views.trainer_requests, name='requests_list'),
    path('requests/update/<int:request_id>/<str:action>/', views.update_request_status, name='update_request_status'),

    path('trainer-add-plans/', views.trainer_add_plans, name='trainer_add_plans'),
]