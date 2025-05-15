from django.urls import path
from . import views

app_name = 'membership'

urlpatterns = [
    path('gyms/search/', views.search_gyms, name='search_gyms'),
    path('buy/<int:gym_id>/', views.buy_membership, name='buy_membership'),
    path('rate/<int:gym_id>/', views.rate_gym, name='rate_gym'),
    path('my/', views.my_memberships, name='my_memberships'),
    path('generate-pdf/<int:membership_id>/', views.generate_membership_pdf, name='generate_membership_pdf'),
    path('gym/<int:gym_id>/', views.gym_detail, name='gym_detail'),

    path('verify-membership-qr/', views.verify_membership_qr, name='verify_membership_qr'),
    path('qr/open/',views.open, name= 'open'),
]
