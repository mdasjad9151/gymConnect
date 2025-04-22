import json
import requests
from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from django.contrib import messages

from django.views.decorators.http import require_POST


from accounts.models import GymUser, Trainer,GymOwner
from .models import TrainerRequest, Gym, GymImage
from .forms import TrainerSelectForm,GymForm,GymImageForm
from accounts.decorators import gym_owner_required
from .utils import get_lat_lon_from_address

@login_required
def gym_owner_deshboard(request):
    owner=  request.user
    profile =  GymOwner.objects.get(id = owner.id)
    
    return render(request, 'gymOwner/deshboard.html',{'profile':profile})

@login_required
def add_trainer(request):
    # Get the logged-in gym owner
    owner=  request.user
    profile =  GymOwner.objects.get(id = owner.id)
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
            'trainers': trainers_to_display,# Only trainers that haven't been requested
            'profile':profile,  
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
@require_POST
def create_trainer_request(request):
    try:
        # Parse JSON from the request body
        data = json.loads(request.body)

        # Get trainer_id from the parsed data
        trainer_id = data.get('trainer_id')
        print(trainer_id)
        if not trainer_id:
            return JsonResponse({'error': 'Trainer ID is required'}, status=400)

        # Check if the trainer exists
        trainer = Trainer.objects.filter(id=trainer_id).first()
        if not trainer:
            return JsonResponse({'error': 'Trainer not found'}, status=404)

        # Get the logged-in gym owner (replace with correct logic if necessary)
        gym_owner = request.user.gymowner

        # Check if a request for this trainer already exists for the gym owner
        if TrainerRequest.objects.filter(gym=gym_owner, trainer=trainer).exists():
            return JsonResponse({'error': 'You have already sent a request to this trainer'}, status=400)

        # Create a new trainer request with default status 'pending'
        TrainerRequest.objects.create(
            gym=gym_owner,
            trainer=trainer,
            request_data="Request for collaboration"  # Customize as needed
        )
        
        # Return success response
        return JsonResponse({'message': 'Request Sent Successfully'}, status=201)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    except AttributeError:
        # Catch attribute error if user does not have a gymowner profile
        return JsonResponse({'error': 'You are not authorized as a gym owner'}, status=403)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@gym_owner_required
def assign_user(request):
    # Get the logged-in user and ensure they are a gym owner
    owner=  request.user
    profile =  GymOwner.objects.get(id = owner.id)
    gym_owner = GymOwner.objects.get(id=request.user.id)

        # Fetch users in the same gym who have trainers from other gyms
    unassigned_users = GymUser.objects.filter(
        gym_id=gym_owner,                       # Same gym as logged-in owner
        # trainer_id__isnull=False,               # Users who have a trainer assigned
    ).exclude(trainer_id__gym_id=gym_owner)     # Exclude users whose trainer belongs to this gym
    # Get all trainers working under this gym owner
    trainers = Trainer.objects.filter(gym_id=gym_owner)

    if request.method == "POST":
        # Get selected user and trainer from POST data
        user_id = request.POST.get("user_id")
        trainer_id = request.POST.get("trainer_id")

        # Assign the trainer to the selected user
        GymUser.objects.filter(id=user_id, gym_id=gym_owner).update(trainer_id=trainer_id)

        # Redirect to the same page to refresh the list
        return redirect("assign_trainer")

    return render(request, "gymowner/assign_trainer.html", {
        "unassigned_users": unassigned_users,
        "trainers": trainers,
        'profile':profile
    })

@login_required
def list_users(request):
    # Get the gym ID from the logged-in user (assuming the gym owner is logged in)
    gym_id =  request.user
    gym_owner = GymOwner.objects.get(id=request.user.id)
    # Fetch users under the logged-in user's gym, with related trainer details
    users = GymUser.objects.filter(gym_id=gym_id).select_related('trainer_id')

    # Prepare the user and trainer data for display
    print(gym_owner.profile_picture)
    user_data = []
    for user in users:
        user_data.append({
            'profile': user.profile_picture,
            "username": user.name,
            'phone': user.contact_no,
            'email':user.email,
            "trainer_name": user.trainer_id.name if user.trainer_id else "No trainer assigned",
        })

    # Render the user data as a response (or you could render it in a template)
    return render(request, 'gymOwner/list_users.html', {"users": user_data,'owner_profile':gym_owner,})

@login_required
def list_trainers(request):
    # Fetch and display all trainers associated with the logged-in user's gym
    gym_id = request.user
    trainers = Trainer.objects.filter(gym_id=gym_id.id)  # Assuming Trainer model is defined
    return render(request, 'gymOwner/trainers_list.html', {'trainers': trainers})



# gym management




@gym_owner_required
def add_gym(request):
    if request.method == 'POST':
        form = GymForm(request.POST, request.FILES)
        images = request.FILES.getlist('images')  # multiple file input with name='images'
        print(images)

        if form.is_valid():
            gym = form.save(commit=False)
            gym.owner = request.user
            full_address = f"{gym.address}, {gym.city}"
            lat, lon = get_lat_lon_from_address(full_address)
            if lat and lon:
                gym.latitude = lat
                gym.longitude = lon
                gym.save()
                
                for img in images:
                    GymImage.objects.create(gym=gym, image=img)
                
                messages.success(request, 'Gym added with coordinates.')
                return redirect('gym_list')
            else:
                messages.error(request, 'Unable to get coordinates from address.')
            # Save gallery images
            
            return redirect('gym_list')  # or any success URL
    else:
        form = GymForm()

    return render(request, 'gymOwner/add_gym.html', {'form': form,})

@gym_owner_required
def gym_list(request):
    gyms = Gym.objects.filter(owner=request.user)
    return render(request, 'gymowner/gym_list.html', {'gyms': gyms})


@gym_owner_required
def edit_gym(request, gym_id):
    gym = get_object_or_404(Gym, id=gym_id, owner=request.user)

    if request.method == 'POST':
        form = GymForm(request.POST, request.FILES, instance=gym)
        image_form = GymImageForm(request.POST, request.FILES)
        
        if form.is_valid():
            form.save()  # Save gym details
            return redirect('gym_list')
            
            # Handling gallery images (if new images are uploaded)
        if image_form.is_valid():
            images = request.FILES.getlist('images')
            for img in images:
                GymImage.objects.create(gym=gym, image=img)
            
            messages.success(request, 'Gym updated successfully.')
            return redirect('gym_list')
    else:
        form = GymForm(instance=gym)
        image_form = GymImageForm()

    return render(request, 'gymOwner/edit_gym.html', {
        'form': form,
        'gym': gym,
        'image_form': image_form,
    })


@gym_owner_required
def delete_gym(request, gym_id):
    gym = get_object_or_404(Gym, id=gym_id, owner=request.user)
    gym.delete()
    messages.success(request, 'Gym deleted successfully.')
    return redirect('gym_list')

    return render(request, 'gymowner/delete_gym.html', {'gym': gym})
def gym_gallery(request, gym_id):
    gym = get_object_or_404(Gym, id=gym_id)
    images = GymImage.objects.filter(gym=gym)
    return render(request, 'gymOwner/gallery.html', {'images': images, 'gym':gym})

