from django import forms
from .models import VideoCourse, CourseVideo

class VideoCourseForm(forms.ModelForm):
    class Meta:
        model = VideoCourse
        fields = ['title', 'description', 'category', 'fitness_level', 'price', 'thumbnail']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full p-2 border rounded-xl'}),
            'description': forms.Textarea(attrs={'class': 'w-full p-2 border rounded-xl', 'rows': 4}),
            'category': forms.Select(attrs={'class': 'w-full p-2 border rounded-xl'}),
            'fitness_level': forms.Select(attrs={'class': 'w-full p-2 border rounded-xl'}),
            'price': forms.NumberInput(attrs={'class': 'w-full p-2 border rounded-xl'}),
            'thumbnail': forms.ClearableFileInput(attrs={'class': 'w-full p-2 border rounded-xl'}),
        }

class CourseVideoForm(forms.ModelForm):
    class Meta:
        model = CourseVideo
        fields = ['title', 'description', 'video_file', 'duration', 'sequence']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full p-2 border rounded-xl'}),
            'description': forms.Textarea(attrs={'class': 'w-full p-2 border rounded-xl', 'rows': 3}),
            'video_file': forms.ClearableFileInput(attrs={'class': 'w-full p-2 border rounded-xl'}),
            'duration': forms.TimeInput(attrs={'class': 'w-full p-2 border rounded-xl', 'type': 'time'}),
            'sequence': forms.NumberInput(attrs={'class': 'w-full p-2 border rounded-xl'}),
        }
