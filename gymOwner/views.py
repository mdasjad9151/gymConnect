import json
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse

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
    form = TrainerSelectForm()
    return render(request, 'gymOwner/add_trainer.html', {'form': form})

@login_required
def get_trainer_details(request, trainer_id):
    trainer = get_object_or_404(Trainer, id=trainer_id)
    print("id  ", trainer.gym_id.gym_name)
    gym_name = trainer.gym_id.gym_name if trainer.gym_id.gym_name else "Unemployed"
    # gym_address = trainer.gym.address if trainer.gym else "N/A"

    trainer_data = {
        'name': trainer.name,
        # 'address': trainer.address,
        # 'contact_no': trainer.contact_no,
        'gym_name': gym_name,
        # 'gym_address': gym_address,
    }
    # print(trainer_data)
    return JsonResponse(trainer_data)


@login_required
def create_trainer_request(request):
    if request.method == "POST":
        try:
            # Parse JSON body to get trainer_id
            data = json.loads(request.body)
            trainer_id = data.get("trainer_id")
            
            trainer = get_object_or_404(Trainer, id=trainer_id)
            gym = get_object_or_404(GymOwner, email=request.user.email)  # assuming user is associated with a gym

            # Create a new TrainerRequest record
            TrainerRequest.objects.create(gym=gym, trainer=trainer, status="NA")

            return JsonResponse({"message": "Request created successfully!"})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)

    return JsonResponse({"error": "Invalid request"}, status=400)


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

