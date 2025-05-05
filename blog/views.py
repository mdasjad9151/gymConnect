from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from .models import Post, Comment, Like, Follow
from .forms import PostForm, CommentForm
import json
@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('blog:post_list')
    else:
        form = PostForm()
    return render(request, 'blog/create_post.html', {'form': form})

def post_list(request):
    post_queryset = Post.objects.all().order_by('-created_at')

    
    paginator = Paginator(post_queryset, 5)  # Show 5 posts per page
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)


    # Enrich each post with user details
    for post in posts:
        user = post.user
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

        # Attach them dynamically
        user.name = name
        user.profile_picture = profile_picture
        user.user_model_name = user_model_name

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('blog:post_list')
    else:
        form = PostForm()

    return render(request, 'blog/post_list.html', {'posts': posts, 'form': form})


@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(user=request.user, post=post)

    if not created:
        like.delete()
        liked = False
    else:
        liked = True

    return JsonResponse({'liked': liked, 'like_count': post.likes.count()})

@require_POST
@login_required
def add_comment(request, post_id):
    try:
        data = json.loads(request.body)  # <-- Parse JSON body
        text = data.get("text", "").strip()
        print(data)
        print(text)
        if text:
            post = get_object_or_404(Post, id=post_id)
            comment = Comment.objects.create(user=request.user, post=post, text=text)

            # Dynamically get the name from the user subclass
            name = None
            if hasattr(comment.user, 'gymuser'):
                name = comment.user.gymuser.name
            elif hasattr(comment.user, 'trainer'):
                name = comment.user.trainer.name
            elif hasattr(comment.user, 'gymowner'):
                name = comment.user.gymowner.gym_name
            elif hasattr(comment.user, 'admin'):
                name = comment.user.admin.name

            return JsonResponse({
                "success": True,
                "comment": {
                    "user": name or "Unknown",
                    "text": comment.text,
                    "created_at": comment.created_at.strftime("%Y-%m-%d %H:%M"),
                }
            })
        else:
            return JsonResponse({"success": False, "error": "Empty comment."})

    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})



@login_required
def load_comments(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.select_related('user').order_by("-created_at")

    comments_data = []
    for c in comments:
        user = c.user
        name = None


        if hasattr(user, 'gymuser'):
            name = user.gymuser.name
        elif hasattr(user, 'trainer'):
            name = user.trainer.name
        elif hasattr(user, 'gymowner'):
            name = user.gymowner.gym_name  # Using gym_name for GymOwner
        
        comments_data.append({
            "user": name or "Unknown",  # Fallback to "Unknown" if name is not found
            "text": c.text,
            "created_at": c.created_at.strftime("%Y-%m-%d %H:%M")
        })

    return JsonResponse({"comments": comments_data})


@login_required
def follow_user(request, user_id):
    user_to_follow = get_object_or_404(User, id=user_id)
    if user_to_follow != request.user:
        follow, created = Follow.objects.get_or_create(user1=request.user, user2=user_to_follow)
        if not created:
            follow.delete()
    return redirect('blog:post_list')
