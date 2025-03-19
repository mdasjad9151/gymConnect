from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Post, Comment, Like, Follow
from .forms import PostForm, CommentForm

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
@login_required
def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('blog:post_list')
    else:
        form = PostForm()
    return render(request, 'blog/post_list.html', {'posts': posts,'form':form})

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

@login_required
def add_comment(request, post_id):
    if request.method == "POST":
        post = get_object_or_404(Post, id=post_id)
        text = request.POST.get("text", "").strip()

        if text:
            comment = Comment.objects.create(user=request.user, post=post, text=text)

            # Dynamically get the name from the user subclass
            name = None
            if hasattr(comment.user, 'gymuser'):
                name = comment.user.gymuser.name
            elif hasattr(comment.user, 'trainer'):
                name = comment.user.trainer.name
            elif hasattr(comment.user, 'gymowner'):
                name = comment.user.gymowner.gym_name  # GymOwner has gym_name
            elif hasattr(comment.user, 'admin'):
                name = comment.user.admin.name  # Admin has name

            return JsonResponse({
                "success": True,
                "comment": {
                    "user": name or "Unknown",  # Fallback to "Unknown" if no name is found
                    "text": comment.text,
                    "created_at": comment.created_at.strftime("%Y-%m-%d %H:%M"),
                }
            })

    return JsonResponse({"success": False, "error": "Invalid comment."})



@login_required
def load_comments(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.select_related('user').order_by("-created_at")

    comments_data = []
    for c in comments:
        user = c.user
        name = None
        print(user)

        if hasattr(user, 'gymuser'):
            name = user.gymuser.name
        elif hasattr(user, 'trainer'):
            name = user.trainer.name
        elif hasattr(user, 'gymowner'):
            name = user.gymowner.gym_name  # Using gym_name for GymOwner
        elif hasattr(user, 'admin'):
            name = user.admin.name  # Admin name if available
        
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
