from django import forms
from .models import Post, Comment

from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'image']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-red-300 bg-white/10 placeholder-black text-black rounded-lg focus:ring-2 focus:ring-red-400 transition backdrop-blur-lg',
                'placeholder': 'Write something interesting...',
                'rows': 5,
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'w-full text-sm text-black m-2  file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-1 file:border-white/10 file:text-sm file:font-semibold file:bg-red-500 file:text-black hover:file:bg-red-600',
            }),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
