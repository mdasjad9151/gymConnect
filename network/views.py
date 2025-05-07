from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.contrib.auth import get_user_model


from .models import ConnectionRequest,PrivateMessage


User = get_user_model()


@login_required
def redirect_to_home(request):
    return redirect("home")

@login_required
def connections(request):
    # Get all accepted connection requests involving the current user
    friends = ConnectionRequest.objects.filter(
        Q(receiver=request.user, status='accepted') |
        Q(sender=request.user, status='accepted')
    )

    connections = []

    for friend_request in friends:
        # Identify the other user in the connection
        other_user = friend_request.sender if friend_request.receiver == request.user else friend_request.receiver
        
        # Default values
        name = None
        profile_picture = None
        user_model_name = None

        # Check and get extended user info
        if hasattr(other_user, 'gymuser'):
            name = other_user.gymuser.name
            profile_picture = other_user.gymuser.profile_picture
            user_model_name = 'gymuser'
        elif hasattr(other_user, 'trainer'):
            name = other_user.trainer.name
            profile_picture = other_user.trainer.profile_picture
            user_model_name = 'trainer'
        elif hasattr(other_user, 'gymowner'):
            name = other_user.gymowner.name
            profile_picture = other_user.gymowner.profile_picture
            user_model_name = 'gymowner'

        # Append enriched user data
        connections.append({
            'id': other_user.id,
            'name': name,
            'profile_picture': profile_picture,
            'user_model_name': user_model_name,
        })

    return render(request, 'chat/connections.html', {'connections': connections})

@login_required
def chat_view(request, username):
    """Render chat page (for API calls, WebSocket handles messages)"""
    return render(request, "chat/index.html", {"selected_friend": username})

@login_required
def add_friends(request):
    # Get all accepted connections (friend list)
    friends = ConnectionRequest.objects.filter(
    Q(receiver=request.user, status__in=['accepted', 'pending']) |
    Q(sender=request.user,   status__in=['accepted', 'pending'])
    )
    sender_ids = friends.values_list('sender_id', flat=True)
    receiver_ids = friends.values_list('receiver_id', flat=True)

    # Combine and deduplicate
    all_related_ids = set(sender_ids) | set(receiver_ids)


    # All other users, excluding self, superusers, and already friends
    users = User.objects.exclude(
        Q(id=request.user.id) |
        Q(is_superuser=True) |
        Q(id__in=all_related_ids)
    )

    # Enrich each user with name, profile picture, and model name
    for user in users:
        user.name = None
        user.profile_picture = None
        user.user_model_name = None

        if hasattr(user, 'gymuser'):
            user.name = user.gymuser.name
            user.profile_picture = user.gymuser.profile_picture
            user.user_model_name = 'gymuser'
        elif hasattr(user, 'trainer'):
            user.name = user.trainer.name
            user.profile_picture = user.trainer.profile_picture
            user.user_model_name = 'trainer'
        elif hasattr(user, 'gymowner'):
            user.name = user.gymowner.name
            user.profile_picture = user.gymowner.profile_picture
            user.user_model_name = 'gymowner'

    return render(request, 'chat/add_friends.html', {'users': users})

@csrf_exempt
@login_required
def send_friend_request(request, user_id):
    print(user_id)
    """Send a friend request"""
    if request.method == "POST":
        receiver = User.objects.get(id=user_id)
        
        if not ConnectionRequest.objects.filter(sender=request.user, receiver=receiver).exists():
            ConnectionRequest.objects.create(sender=request.user, receiver=receiver)
            return JsonResponse({"success": True})
        return JsonResponse({"success": False, "error": "Request already sent."})
    return JsonResponse({"success": False, "error": "Post request.."})

@login_required
def show_requests(request):
    """Show all pending friend requests received by the user"""
    friend_requests = ConnectionRequest.objects.filter(receiver=request.user, status="pending")

    for friend_request in friend_requests:
        user = friend_request.receiver if friend_request.sender == request.user else friend_request.sender

        name = None
        profile_picture = None
        user_model_name = None

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

        # Attach them to the request for access in template
        friend_request.other_user = user
        friend_request.name = name
        friend_request.profile_picture = profile_picture
        friend_request.user_model_name = user_model_name

    return render(request, "chat/friend_requests.html", {
        "friend_requests": friend_requests
    })


@login_required
def accept_friend_request(request, request_id):
    """Accept a friend request (change status to 'accepted')"""
    friend_request = get_object_or_404(ConnectionRequest, id=request_id, receiver=request.user)
    
    if request.method == "POST":
        friend_request.status = "accepted"
        friend_request.save()
        return JsonResponse({"success": True, "message": "Friend request accepted!"})

    return JsonResponse({"success": False, "error": "Invalid request."})

@login_required
def reject_friend_request(request, request_id):
    """Reject a friend request (delete the row)"""
    friend_request = get_object_or_404(ConnectionRequest, id=request_id, receiver=request.user)

    if request.method == "POST":
        friend_request.delete()
        return JsonResponse({"success": True, "message": "Friend request rejected!"})

    return JsonResponse({"success": False, "error": "Invalid request."})


@login_required
def fetch_messages(request, username):
    """ Fetch previous messages between logged-in user and selected user. """
    selected_user = get_object_or_404(User, username=username)
    logged_user = request.user

    # Get messages where sender or receiver is either of the users
    messages = PrivateMessage.objects.filter(
        sender__in=[logged_user, selected_user],
        receiver__in=[logged_user, selected_user]
    ).order_by('timestamp')

    # Serialize messages
    message_list = [
        {
            'message': msg.message,
            'sender': msg.sender.username,
            'receiver': msg.receiver.username,
            'timestamp': msg.timestamp.strftime("%Y-%m-%d %H:%M"),
        } for msg in messages
    ]

    return JsonResponse({'messages': message_list})