from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import (
    AdminRegistrationForm,
    GymOwnerRegistrationForm,
    TrainerRegistrationForm,
    GymUserRegistrationForm,
    CustomLoginForm,
)

def register_admin(request):
    if request.method == 'POST':
        form = AdminRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('account:login')
    else:
        form = AdminRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form, 'user_type': 'Admin'})

def register_gym_owner(request):
    if request.method == 'POST':
        form = GymOwnerRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('accounts:login')
    else:
        form = GymOwnerRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form, 'user_type': 'Gym Owner'})

def register_trainer(request):
    if request.method == 'POST':
        form = TrainerRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('accounts:login')
    else:
        form = TrainerRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form, 'user_type': 'Trainer'})

def register_gym_user(request):
    if request.method == 'POST':
        form = GymUserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('accounts:login')
    else:
        form = GymUserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form, 'user_type': 'Gym User'})

def user_login(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('accounts:dashboard')
    else:
        form = CustomLoginForm()
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    return redirect('accounts:login')



# Websocket Auth check.abs
@login_required
def check_auth(request):
    return JsonResponse({"user": request.user.id})


@login_required
def dashboard(request):
    user = request.user  # Get the logged-in user
    
    # Determine user type
    if hasattr(user, 'admin'):
        user_type = f"Admin: {user.name}"

    elif hasattr(user, 'gymowner'):
        print(hasattr(user, 'gymowner'))
        return redirect('gym_owner_deshboard')

    elif hasattr(user, 'trainer'):
        return redirect('trainer_dashboard')

    elif hasattr(user, 'gymuser'):
        return redirect('user_dashboard')

    context = {'user_type': user_type}
    return JsonResponse({'sucess':'failed', 'message':'user type does not exist'})

