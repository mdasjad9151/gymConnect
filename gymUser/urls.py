from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from . import views 


urlpatterns = [
    path('dashboard/', views.user_dashboard, name='user_dashboard'),  # URL for the dashboard
    path('join-gym/', views.join_gym, name='join_gym'),              # URL for the 'Join' button
    path('join-gym/<int:gym_id>/', views.join_selected_gym, name='join_selected_gym'),
    path('view-plan/', views.view_plan, name='view_plan'),             # URL for the 'Plan' button
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)