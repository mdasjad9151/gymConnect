# forms.py
from django import forms
from accounts.models import Trainer

from membership.models import Gym  # Your Gym model is here

class TrainerSelectForm(forms.Form):
    trainer = forms.ModelChoiceField(
        queryset=Trainer.objects.all(),
        empty_label="Select Trainer",
        widget=forms.Select(attrs={"class": "form-select w-full p-2 border border-gray-300 rounded"}),
    )





class GymForm(forms.ModelForm):
    class Meta:
        model = Gym
        fields = ['name', 'address', 'city', 'latitude', 'longitude', 'price_per_day']
