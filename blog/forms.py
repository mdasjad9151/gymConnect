from django import forms
from .models import Post, Comment

from django import forms
from .models import Post

from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'w-full px-4 py-2 border border-red-300 bg-white/10 placeholder-black text-black rounded-lg focus:ring-2 focus:ring-red-400 transition backdrop-blur-lg',
            'placeholder': 'Write something interesting...',
            'rows': 5,
        }),
        required=False
    )

    image = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={
            'class': 'w-full text-sm text-black m-2 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-1 file:border-white/10 file:text-sm file:font-semibold file:bg-red-500 file:text-black hover:file:bg-red-600',
        }),
        required=False
    )

    class Meta:
        model = Post
        fields = []  # Do not use 'data' directly here

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Populate form fields from data if instance exists
        if self.instance and self.instance.data:
            self.fields['content'].initial = self.instance.data.get('content', '')
            self.fields['image'].initial = self.instance.data.get('image', '')

    def clean(self):
        cleaned_data = super().clean()
        content = cleaned_data.get('content', '')
        image = cleaned_data.get('image', None)

        self.cleaned_data['data'] = {
            'content': content,
            'image': image.name if image else self.instance.data.get('image') if self.instance and self.instance.data else None
        }

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)

        image = self.cleaned_data.get('image')
        if image:
            instance.image = image  # only needed if ImageField is present
            image_path = f"Post/{image.name}"  # Add directory prefix manually
        else:
            image_path = self.cleaned_data['data'].get('image')

        instance.data = {
            'content': self.cleaned_data['data']['content'],
            'image': image_path
        }

        if commit:
            instance.save()
        return instance


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
