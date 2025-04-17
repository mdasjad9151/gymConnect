from django.shortcuts import render
from blog.models import Post
from blog.forms import PostForm

def home(request):
    posts = Post.objects.all().order_by('-created_at')
    print(posts)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('blog:post_list')
    else:
        form = PostForm()
    return render(request, 'core/home.html' ,{'posts': posts,'form':form})


