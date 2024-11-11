from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,Http404,JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

from accounts.models import GymUser
from gymOwner.models import TrainerRequest
from .models import Plan
from .forms import PlanForm

@login_required
def trainer_dashboard(request):
    # Render the main dashboard with buttons
    return render(request, 'trainer/trainer_dashboard.html')


@login_required
def trainer_requests(request):
    # Fetch requests for the logged-in trainer
    trainer_requests = TrainerRequest.objects.filter(trainer=request.user, status='pending')
    # print(request.user)
    return render(request, 'trainer/requests_list.html', {
        'trainer_requests': trainer_requests,
    })


@login_required
def update_request_status(request, request_id, action):
    # Get the specific TrainerRequest and ensure the current user is the trainer for this request
    trainer_request = get_object_or_404(TrainerRequest, id=request_id, trainer=request.user)

    if action == 'accept':
        trainer_request.status = 'accepted'
        
        # Update the gym_id in the trainer table if accepted
        trainer = trainer_request.trainer
        trainer.gym_id = trainer_request.gym  # Set the trainer's gym to the gym of the request
        trainer.save()  # Save the trainer with the updated gym_id

    elif action == 'reject':
        trainer_request.status = 'rejected'
        
    else:
        raise Http404("Invalid action.")

    # Save the status update and delete the request instance
    trainer_request.save()
    trainer_request.delete()  # Remove the request after updating its status

    return redirect('trainer_requests')


@login_required
def trainer_add_plans(request):
    trainer = request.user
    gym_users = GymUser.objects.filter(trainer_id=trainer)

    return render(request, 'trainer/add_plans.html', {
        'gym_users': gym_users,
    })

@login_required
def get_user_plan(request, user_id):
    try:
        gym_user = GymUser.objects.get(id=user_id, trainer_id=request.user)
        plan = Plan.objects.filter(user_id=gym_user).first()

        data = {
            'monday_workout': plan.monday_workout if plan else '',
            'tuesday_workout': plan.tuesday_workout if plan else '',
            'wednesday_workout': plan.wednesday_workout if plan else '',
            'thursday_workout': plan.thursday_workout if plan else '',
            'friday_workout': plan.friday_workout if plan else '',
            'saturday_workout': plan.saturday_workout if plan else '',
            'breakfast': plan.breakfast if plan else '',
            'lunch': plan.lunch if plan else '',
            'dinner': plan.dinner if plan else '',
            'preworkout_diet': plan.preworkout_diet if plan else '',
            'update_date': plan.update_date if plan else 'NA',
        }

        return JsonResponse(data)

    except GymUser.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

@login_required
def update_plan(request):
    if request.method == 'POST':
        gym_user_id = int(request.POST.get('gym_user_id'))
        print(gym_user_id)
        gym_user = GymUser.objects.get(id=gym_user_id, trainer_id=request.user)
        plan, created = Plan.objects.get_or_create(user_id=gym_user.id)

        # Extract data from the request and update the plan
        plan.monday_workout = request.POST.get('monday_div')
        plan.tuesday_workout = request.POST.get('tuesday_div')
        plan.wednesday_workout = request.POST.get('wednesday_div')
        plan.thursday_workout = request.POST.get('thursday_div')
        plan.friday_workout = request.POST.get('friday_div')
        plan.saturday_workout = request.POST.get('saturday_div')
        plan.breakfast = request.POST.get('breakfast_div')
        plan.lunch = request.POST.get('lunch_div')
        plan.dinner = request.POST.get('dinner_div')
        plan.preworkout_diet = request.POST.get('preworkout_diet_div')

        plan.save()
        return JsonResponse({'success': True})
    return JsonResponse({'error': 'Invalid request'}, status=400)