from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from accounts.decorators import trainer_required
from .models import Blog, Comment, Like, Follow
from .forms import BlogForm
import json


@trainer_required
# @login_required
def create_blog(request):
    if request.method == "POST":
        form = BlogForm(request.POST)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.trainer = request.user.trainer  # Ensure the logged-in user is a trainer
            blog.save()
            # return redirect("blog_list")  # Redirect to the blog list page after successful creation
            return HttpResponse("saved")
        else:
            return render(request, "blog/create_blog.html", {"form": form})  # Re-render form with errors

    else:
        form = BlogForm()
        return render(request, "blog/create_blog.html", {"form": form})
# @csrf_exempt
# def create_blog(request):
#     if request.method == "POST":
#         data = json.loads(request.body)
#         blog = Blog.objects.create(
#             trainer=request.user,
#             title=data["title"],
#             content=data["content"]
#         )
#         return JsonResponse({"message": "Blog created successfully!", "blog_id": blog.id})

@login_required
@csrf_exempt
def edit_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id, trainer=request.user)
    if request.method == "POST":
        data = json.loads(request.body)
        blog.title = data["title"]
        blog.content = data["content"]
        blog.save()
        return JsonResponse({"message": "Blog updated successfully!"})

@login_required
@csrf_exempt
def delete_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id, trainer=request.user)
    if request.method == "DELETE":
        blog.delete()
        return JsonResponse({"message": "Blog deleted successfully!"})

@login_required
@csrf_exempt
def add_comment(request, blog_id):
    if request.method == "POST":
        data = json.loads(request.body)
        blog = get_object_or_404(Blog, id=blog_id)
        comment = Comment.objects.create(
            user=request.user,
            blog=blog,
            text=data["text"]
        )
        return JsonResponse({"message": "Comment added successfully!", "comment_id": comment.id})

@login_required
@csrf_exempt
def like_blog(request, blog_id):
    print(blog_id)
    blog = get_object_or_404(Blog, id=blog_id)
    like, created = Like.objects.get_or_create(user=request.user, blog=blog)
    if not created:
        like.delete()
        return JsonResponse({"message": "Like removed"})
    return JsonResponse({"message": "Blog liked"})

@login_required
@csrf_exempt
def follow_trainer(request, trainer_id):
    trainer = get_object_or_404(User, id=trainer_id)
    follow, created = Follow.objects.get_or_create(user=request.user, trainer=trainer)
    if not created:
        follow.delete()
        return JsonResponse({"message": "Unfollowed"})
    return JsonResponse({"message": "Following trainer"})



def blog_list(request):
    blogs = Blog.objects.all().order_by('-created_at')  # Show newest blogs first
    return render(request, "blog/blog_list.html", {"blogs": blogs})


def blog_detail(request, slug):
    blog = get_object_or_404(Blog, id=slug)  # Fetch blog by slug
    print(blog)
    return render(request, "blog/blog_detail.html", {"blog": blog})