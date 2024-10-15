from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from accounts.models import GymUser, Trainer

# Create your views here.
@login_required
def gym_owner_deshboard(request):
    
    return render(request, 'gymOwner/deshboard.html')

@login_required
def add_user(request):
    # Logic to add a user
    return HttpResponse("add user")

@login_required
def add_trainer(request):
    # Logic to add a trainer
    return HttpResponse("add trainer ")

@login_required
def list_users(request):
    # Fetch and display all users
    users = GymUser.objects.all()  # Assuming User model is defined
    return HttpResponse(users)

@login_required
def list_trainers(request):
    # Fetch and display all trainers
    trainers = Trainer.objects.all()  # Assuming Trainer model is defined
    return HttpResponse(trainers)

