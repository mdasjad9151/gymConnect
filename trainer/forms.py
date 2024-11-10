from django import forms
from .models import Plan

class PlanForm(forms.ModelForm):
    class Meta:
        model = Plan
        fields = [
            'user',
            'monday_workout',
            'tuesday_workout',
            'wednesday_workout',
            'thursday_workout',
            'friday_workout',
            'saturday_workout',
            'breakfast',
            'lunch',
            'dinner',
            'preworkout_diet',
        ]
        widgets = {
            'monday_workout': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Workout details for Monday'}),
            'tuesday_workout': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Workout details for Tuesday'}),
            'wednesday_workout': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Workout details for Wednesday'}),
            'thursday_workout': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Workout details for Thursday'}),
            'friday_workout': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Workout details for Friday'}),
            'saturday_workout': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Workout details for Saturday'}),
            'breakfast': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Diet details for Breakfast'}),
            'lunch': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Diet details for Lunch'}),
            'dinner': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Diet details for Dinner'}),
            'preworkout_diet': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Diet details for Pre-workout'}),
        }
