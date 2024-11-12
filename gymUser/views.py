from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse,HttpResponse

from accounts.models import GymUser, GymOwner
from trainer.models import Plan

@login_required
def user_dashboard(request):
    user =  request.user
    profile =  GymUser.objects.get(id =  user.id)
    return render(request, 'gymUser/deshboard.html',{'profile': profile})  

@login_required
def join_gym(request):
    # Get the current user and check if they are a GymUser
    user = request.user
    profile =  GymUser.objects.get(id =  user.id)
    gym_user = GymUser.objects.filter(id=user.id).first()
    
    # Fetch gyms in the same city as the GymUser
    gyms_in_city = GymOwner.objects.filter(city=gym_user.city).exclude(id=gym_user.gym_id_id)
    
    return render(request, 'gymUser/join_gym.html', {
        'gyms': gyms_in_city,
        'gym_user': gym_user,
        'profile': profile,
    })

@login_required
def join_selected_gym(request, gym_id):
    # Get the current user and check if they are a GymUser
    user = request.user
    gym_user = get_object_or_404(GymUser, id=user.id)

    # Update gym_id of GymUser with selected gym's ID
    selected_gym = get_object_or_404(GymOwner, id=gym_id)
    gym_user.gym_id = selected_gym
    gym_user.save()

    return JsonResponse({"success": True})

def view_plan(request):
    user = request.user
    profile =  GymUser.objects.get(id =  user.id)
    gym_user = request.user.gymuser
    try:
        user_plan = Plan.objects.get(user=gym_user)
    except Plan.DoesNotExist:
        user_plan = None  # If no plan exists for the user, handle it in the template

    return render(request, 'gymUser/user_plan.html', {
        'user_plan': user_plan,
        'profile': profile,
    })