from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required

from django.db.models import Avg
from datetime import date, timedelta
from gymOwner.models import Gym,GymRating, GymImage
from .models import Membership
from gymOwner.utils import get_lat_lon_from_address
from .utils import calculate_distance
from accounts.models import GymOwner, Trainer, GymUser
import uuid

@login_required
def search_gyms(request):
    gyms_in_radius = []
    user_lat = user_lon = None

    if request.method == "GET":
        radius = float(request.GET.get('radius', 10))  # default 10km
        address = request.GET.get('address')
        lat = request.GET.get('lat')
        lon = request.GET.get('lon')

        if address:
            try:
                user_lat, user_lon = get_lat_lon_from_address(address)
            except Exception as e:
                return render(request, 'membership/nearby_gyms.html', {
                    'error': f"Error finding location from address: {str(e)}"
                })
        elif lat and lon:
            try:
                user_lat = float(lat)
                user_lon = float(lon)
            except ValueError:
                return render(request, 'membership/nearby_gyms.html', {
                    'error': "Invalid latitude/longitude values."
                })

        if user_lat and user_lon:
            for gym in Gym.objects.all():
                dist = calculate_distance(user_lat, user_lon, gym.latitude, gym.longitude)
                if dist <= radius:
                    gyms_in_radius.append((gym, round(dist, 2)))
            gyms_in_radius.sort(key=lambda x: x[1])

    return render(request, 'membership/nearby_gyms.html', {
        'gyms': gyms_in_radius,
        # 'gym_id': gym.id
    })



@login_required
def buy_membership(request, gym_id):
    gym = get_object_or_404(Gym, id=gym_id)

    if request.method == 'POST':
        duration = request.POST.get('duration')  # day/month/year
        count = int(request.POST.get('count'))   # number
        user = request.user

        start_date = date.today()

        # Determine the expiry based on duration and count
        if duration == 'day':
            delta = timedelta(days=count)
        elif duration == 'month':
            delta = timedelta(days=30 * count)
        elif duration == 'year':
            delta = timedelta(days=365 * count)
        else:
            delta = timedelta(days=1)

        expire_date = start_date + delta

        Membership.objects.create(
            user=user,
            gym=gym,
            token_code=str(uuid.uuid4())[:10],
            paid=True,
            start_date=start_date,
            expire_date=expire_date
        )
        return redirect('membership:my_memberships')  # or any thank you page

    return render(request, 'membership/buy_membership.html', {
        'gym': gym
    })

@login_required
def rate_gym(request, gym_id):
    gym = get_object_or_404(Gym, id=gym_id)
    print(gym)

    if request.method == 'POST':
        rating = int(request.POST.get('rating'))
        review = request.POST.get('review')

        GymRating.objects.update_or_create(
            user=request.user,
            gym=gym,
            defaults={'rating': rating, 'review': review}
        )

        # Recalculate average rating
        ratings = gym.ratings.all()
        gym.average_rating = ratings.aggregate(Avg('rating'))['rating__avg']
        gym.rating_count = ratings.count()
        gym.save()

        return redirect('membership:my_memberships')

    return render(request, 'membership/rate_gym.html', {'gym': gym})

@login_required
def my_memberships(request):
    memberships = Membership.objects.filter(user=request.user).select_related('gym')
    rated_gym_ids = GymRating.objects.filter(user=request.user).values_list('gym_id', flat=True)

    return render(request, 'membership/my_memberships.html', {
        'memberships': memberships,
        'rated_gym_ids': list(rated_gym_ids),
    })


def gym_detail(request, gym_id):

    gym = Gym.objects.get(id=gym_id)
    ratings = GymRating.objects.filter(gym=gym).select_related('user')
    images = GymImage.objects.filter(gym=gym)

    processed_ratings = []

    for rating in ratings:
        user = rating.user
        name = "Anonymous"
        profile_picture = None
        user_model_name = "baseuser"

        # Check for reverse one-to-one relations
        if hasattr(user, 'gymuser'):
            name = user.gymuser.name
            profile_picture = user.gymuser.profile_picture
            user_model_name = 'gymuser'
        elif hasattr(user, 'trainer'):
            name = user.trainer.name
            profile_picture = user.trainer.profile_picture
            user_model_name = 'trainer'
        elif hasattr(user, 'gymowner'):
            name = user.gymowner.name
            profile_picture = user.gymowner.profile_picture
            user_model_name = 'gymowner'

        # Attach to user object for template
        user.name = name
        user.profile_picture = profile_picture
        user.user_model_name = user_model_name
        rating.user = user
        processed_ratings.append(rating)

    avg_rating = ratings.aggregate(avg=Avg('rating'))['avg']
    average_rating = round(avg_rating, 1) if avg_rating else 0
    review_count = ratings.count()

    return render(request, 'membership/gym_detail.html', {
        'gym': gym,
        'ratings': processed_ratings,
        'images': images,
        'average_rating': average_rating,
        'review_count': review_count,
    })
