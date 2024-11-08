from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,Http404,JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

from accounts.models import GymUser
from gymOwner.models import TrainerRequest
from .models import Plan

@login_required
def trainer_dashboard(request):
    # Render the main dashboard with buttons
    return render(request, 'trainer/trainer_dashboard.html')


@login_required
def trainer_requests(request):
    # Fetch requests for the logged-in trainer
    trainer_requests = TrainerRequest.objects.filter(trainer=request.user,status='pending')
    # print(request.user)
    return render(request, 'trainer/requests_list.html', {
        'trainer_requests': trainer_requests,
    })


@login_required
def update_request_status(request, request_id, action):
    trainer_request = get_object_or_404(TrainerRequest, id=request_id, trainer=request.user)
    
    if action == 'accept':
        trainer_request.status = 'accepted'
    elif action == 'reject':
        trainer_request.status = 'rejected'
    else:
        raise Http404("Invalid action.")
    
    trainer_request.save()
    return redirect('trainer_requests')


@login_required
def trainer_add_plans(request):
    # Assuming the logged-in user is a trainer
    trainer = request.user
    print(trainer)
    # Fetch all users associated with this trainer
    gym_users = GymUser.objects.filter(trainer_id=trainer)
    print(gym_users)
    return render(request, 'trainer/add_plans.html', {
        'gym_users': gym_users,
    })

@csrf_exempt
@login_required
def submit_plan(request):
    if request.method == "POST":
        user_id = request.POST.get("user_id")
        workout = request.POST.get("workout")
        diet = request.POST.get("diet")

        # Fetch the GymUser instance
        user = get_object_or_404(GymUser, id=user_id)

        # Create or update the Plan record
        Plan.objects.update_or_create(
            user=user,
            defaults={
                'workout': workout,
                'diet': diet,
                'update_date': timezone.now()
            }
        )

        return JsonResponse({"status": "success"})
    return JsonResponse({"status": "failed"}, status=400)

@login_required
def get_user_plans(request, user_id):
    user = get_object_or_404(GymUser, id=user_id)
    plan = Plan.objects.filter(user_id=user).first()
    
    if request.method == 'GET':
        # Fetch previous plan data or set to 'NA' if it doesn’t exist
        previous_workout = plan.workout if plan else 'NA'
        previous_diet = plan.diet if plan else 'NA'
        update_date = plan.update_date if plan else 'NA'

        return JsonResponse({
            'previous_workout': previous_workout,
            'previous_diet': previous_diet,
            'update_date': update_date
        })

    elif request.method == 'POST':
        # Handle form submission from popup
        workout = request.POST.get('workout')
        diet = request.POST.get('diet')
        
        # Save or update the plan for this user
        plan, created = Plan.objects.update_or_create(
            user_id=user,
            defaults={'workout': workout, 'diet': diet, 'updated_date': datetime.now()}
        )
        
        return JsonResponse({'success': True})