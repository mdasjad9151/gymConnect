from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from PIL import Image
from django.http import FileResponse, Http404
from django.core.files.storage import default_storage
from django.db.models import Avg
from datetime import date, timedelta
from gymOwner.models import Gym,GymRating, GymImage
from .models import Membership
from gymOwner.utils import get_lat_lon_from_address
from .utils import calculate_distance
from accounts.models import GymOwner, Trainer, GymUser
import io
import qrcode
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


def get_user_display_name(user):
    try:
        if hasattr(user, 'gymuser'):
            return user.gymuser.name,user.gymuser.profile_picture
        elif hasattr(user, 'gymowner'):
            return user.gymowner.name,user.gymuser.profile_picture
        elif hasattr(user, 'trainer'):
            return user.trainer.name,user.gymuser.profile_picture
        else:
            return user.email
    except Exception:
        return user.email

@login_required
def generate_membership_pdf(request, membership_id):
    try:
        membership = Membership.objects.select_related('gym', 'user').get(id=membership_id, user=request.user)
    except Membership.DoesNotExist:
        raise Http404("Membership not found")

    # Create QR code
    qr_img = qrcode.make(membership.token_code)
    if qr_img.mode != 'RGB':
        qr_img = qr_img.convert('RGB')

    # Prepare profile picture
    profile_img = None
    user_info = get_user_display_name(membership.user)
    image_field_file = user_info[1]
    if image_field_file and default_storage.exists(image_field_file.name):
        with default_storage.open(image_field_file.name, 'rb') as f:
            profile_img = Image.open(f)
            if profile_img.mode != 'RGB':
                profile_img = profile_img.convert('RGB')

    # Create PDF
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)

    # Header
    p.setFont("Helvetica-Bold", 20)
    p.drawString(50, 740, "GymConnect Membership Details")
    p.line(50, 680, 550, 680)

    # Left: Text Info
    p.setFont("Helvetica", 12)
    y = 640
    line_height = 20
    p.drawString(50, y, f"Name: {user_info[0]} ({membership.user.email})")
    y -= line_height
    p.drawString(50, y, f"Gym: {membership.gym.name}")
    y -= line_height
    p.drawString(50, y, f"Token Code: {membership.token_code}")
    y -= line_height
    p.drawString(50, y, f"Paid: {'Yes' if membership.paid else 'No'}")
    y -= line_height
    p.drawString(50, y, f"Start Date: {membership.start_date}")
    y -= line_height
    p.drawString(50, y, f"Expire Date: {membership.expire_date}")

    # Right Top: QR Code
    p.drawInlineImage(qr_img, 400, 500, width=200, height=200)
    
    # Right Bottom: Profile Picture
    if profile_img:
        p.drawInlineImage(profile_img, 400, 400, width=130, height=130)

    p.showPage()
    p.save()
    buffer.seek(0)

    return FileResponse(buffer, as_attachment=True, filename=f"membership_{membership.gym.name}.pdf")






@login_required
def verify_membership_qr(request):
    if request.method == 'POST':
        token = request.POST.get('token_code')
        try:
            membership = Membership.objects.select_related('user', 'gym').get(token_code=token)


            data = {
                'success': True,
                'user_email': membership.user.email,
                'gym_name': membership.gym.name,
                'token_code': membership.token_code,
                'paid': membership.paid,
                'start_date': membership.start_date.strftime("%Y-%m-%d"),
                'expire_date': membership.expire_date.strftime("%Y-%m-%d"),
                'status': 'Active' if membership.start_date <= date.today() <= membership.expire_date else 'Expired',
            }
            return JsonResponse(data)
        except Membership.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Invalid token.'})
    return JsonResponse({'success': False, 'message': 'Invalid request.'})

def open(request):
    return render(request, 'membership/verify_membership.html')