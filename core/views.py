from django.shortcuts import render, redirect
from blog.models import Post
from blog.forms import PostForm

def home(request):
    
    return redirect('blog:post_list')


