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
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-400 transition',
                'placeholder': 'Write something interesting...',
                'rows': 1,
            }),
            'image': forms.ClearableFileInput(attrs={

                  # JavaScript function for file name display
            }),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
