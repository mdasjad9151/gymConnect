from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,Http404
from django.contrib.auth.decorators import login_required

from gymOwner.models import TrainerRequest

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
    # Placeholder for the add plans view
    return HttpResponse("plans")
