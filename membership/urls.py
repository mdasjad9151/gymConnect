from django.urls import path
from . import views

app_name = 'membership'

urlpatterns = [
    path('gyms/search/', views.search_gyms, name='search_gyms'),
    path('buy/<int:gym_id>/', views.buy_membership, name='buy_membership'),
    path('rate/<int:gym_id>/', views.rate_gym, name='rate_gym'),
    path('my/', views.my_memberships, name='my_memberships'),
    path('gym/<int:gym_id>/', views.gym_detail, name='gym_detail'),
]
