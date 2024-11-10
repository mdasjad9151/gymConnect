import json
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from accounts.models import GymUser, Trainer,GymOwner
from .models import TrainerRequest
from .forms import TrainerSelectForm

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
    # Get the logged-in gym owner
    gym_owner = request.user.gymowner

    # Get all trainers who are not associated with the logged-in gym owner
    trainers = Trainer.objects.exclude(gym_id=gym_owner)

    # Get all trainer requests that have been sent by the gym owner
    trainer_requests = TrainerRequest.objects.filter(gym=gym_owner)

    # Prepare a set of trainer IDs that have already been requested
    requested_trainers = {trainer_request.trainer.id for trainer_request in trainer_requests}

    # Filter out trainers who have already been requested
    trainers_to_display = trainers.exclude(id__in=requested_trainers)

    # Pass the filtered trainers to the template
    return render(
        request,
        'gymOwner/add_trainer.html',
        {
            'trainers': trainers_to_display,  # Only trainers that haven't been requested
        }
    )

@login_required
def get_trainer_details(request, trainer_id):
    trainer = get_object_or_404(Trainer, id=trainer_id)
    gym_name = trainer.gym_id.gym_name if trainer.gym_id else "Unemployed"
    full_address = f"{trainer.address}, {trainer.city}, {trainer.state}"
    
    trainer_data = {
        'name': trainer.name,
        'image_url': trainer.profile_picture.url if trainer.profile_picture else None,
        'address': full_address,
        'contact_no': trainer.contact_no,
        'gym_name': gym_name,
        'gym_address': gym_name,
        'certificate_link': trainer.certificate_image.url,
    }
    
    return JsonResponse(trainer_data)

@login_required
def create_trainer_request(request):
    try:
        # Parse JSON from the request body
        data = json.loads(request.body)

        # Get trainer_id from the parsed data
        trainer_id = data.get('trainer_id')

        # Check if trainer_id is valid
        if not trainer_id:
            return JsonResponse({'error': 'Trainer ID is required'}, status=400)

        # Check if the trainer exists in the database
        trainer = Trainer.objects.filter(id=trainer_id).first()
        if not trainer:
            return JsonResponse({'error': 'Trainer not found'}, status=404)

        # Get the logged-in gym owner (assuming gym_owner is related to the user)
        gym_owner = request.user.gymowner  # Replace with correct logic if necessary

        # Check if a request for this trainer already exists
        existing_request = TrainerRequest.objects.filter(gym=gym_owner, trainer=trainer).exists()
        if existing_request:
            return JsonResponse({'error': 'You have already sent a request to this trainer'}, status=400)

        # Create a new trainer request
        trainer_request = TrainerRequest.objects.create(
            gym=gym_owner,
            trainer=trainer,
            request_data="Request for collaboration",  # Customize if you need more info
            status='pending'  # Default status is 'pending'
        )

        # Return success message
        return JsonResponse({'message': 'Request Sent Successfully'}, status=201)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


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

