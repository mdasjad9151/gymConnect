from django.shortcuts import render,redirect
from django.http import HttpResponse,Http404
from django.contrib.auth.decorators import login_required

from gymOwner.models import TrainerRequest

@login_required
def trainer_dashboard(request):
    # Render the main dashboard with buttons
    return render(request, 'trainer/trainer_dashboard.html')


@login_required
def trainer_requests(request):
    # Assuming trainer is a user, fetch the requests for that trainer
    trainer_requests = TrainerRequest.objects.filter(trainer=request.user)

    return render(request, 'trainer/requests_list.html', {
        'trainer_requests': trainer_requests,
    })


@login_required
def update_request_status(request, request_id, action):
    try:
        trainer_request = TrainerRequest.objects.get(id=request_id, trainer=request.user)
    except TrainerRequest.DoesNotExist:
        raise Http404("Request not found or you're not authorized to update it.")
    
    if action == 'accept':
        trainer_request.status = 'accepted'
    elif action == 'reject':
        trainer_request.status = 'rejected'
    else:
        raise Http404("Invalid action.")
    
    trainer_request.save()

    return redirect('trainer:requests_list')  # Redirect to the requests list page after updating



@login_required
def trainer_add_plans(request):
    # Placeholder for the add plans view
    return HttpResponse("plans")
