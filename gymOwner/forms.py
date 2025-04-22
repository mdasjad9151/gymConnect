# forms.py
from django import forms
from accounts.models import Trainer

from .models import Gym, GymImage  # Your Gym model is here

class TrainerSelectForm(forms.Form):
    trainer = forms.ModelChoiceField(
        queryset=Trainer.objects.all(),
        empty_label="Select Trainer",
        widget=forms.Select(attrs={"class": "w-full p-2 rounded-md border border-gray-300 backbrop-blur-sm bg-white/30"}),
    )


class GymForm(forms.ModelForm):
    class Meta:
        model = Gym
        fields = ['name', 'address', 'city', 'state', 'pincode','opening_time', 'closing_time' ,'gym_logo','description', 'price_per_day']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full p-2 rounded-md border border-gray-300 backbrop-blur-sm bg-white/30',
                'placeholder': 'Enter gym name'
            }),
            'address': forms.Textarea(attrs={
                'class': 'w-full p-2 rounded-md border border-gray-300 backbrop-blur-sm bg-white/30',
                'placeholder': 'Enter full address',
                'rows': 2
            }),
            'city': forms.TextInput(attrs={
                'class': 'w-full p-2 rounded-md border border-gray-300 backbrop-blur-sm bg-white/30',
                'placeholder': 'Enter city name'
            }),
            'state': forms.TextInput(attrs={
                'class': 'w-full p-2 rounded-md border border-gray-300 backbrop-blur-sm bg-white/30',
                'placeholder': 'Enter state name'
            }),
            'pincode': forms.TextInput(attrs={
                'class': 'w-full p-2 rounded-md border border-gray-300 backbrop-blur-sm bg-white/30',
                'placeholder': 'Enter pincode'
            }),
            'price_per_day': forms.NumberInput(attrs={
                'class': 'w-full p-2 rounded-md border border-gray-300 backbrop-blur-sm bg-white/30',
                'placeholder': 'Price per day (in ₹)'
            }),
            'gym_logo': forms.ClearableFileInput(attrs={
                'class': 'w-full p-2 border border-gray-300 file:bg-[#51b6ab] file:text-black file:rounded-md backbrop-blur-sm bg-white/30',
            }),
            'description': forms.TextInput(attrs = {
                'class': 'w-full p-2 border border-gray-300 file:bg-[#51b6ab] file:text-black file:rounded-md backbrop-blur-sm bg-white/30',
            }),
            'opening_time' : forms.TimeInput(attrs={
                'class': 'w-full p-2 border border-gray-300 file:bg-[#51b6ab] file:text-black file:rounded-md backdrop-blur-sm bg-white/30',
                   'type': 'time'  # Ensures browser shows time picker
                    }),


            'closing_time' : forms.TimeInput(attrs={
                    'class': 'w-full p-2 border border-gray-300 file:bg-[#51b6ab] file:text-black file:rounded-md backdrop-blur-sm bg-white/30',
                    'type': 'time'
                    })

        }

class GymImageForm(forms.ModelForm):
    class Meta:
        model = GymImage
        fields = ['image']
        widgets = {
            'image': forms.ClearableFileInput(attrs={
                'class': 'w-full file:bg-[#51b6ab] file:text-black file:px-4 file:py-2 file:rounded-lg file:border-0 backbrop-blur-sm bg-white/30' ,
                'placeholder': 'Upload gym gallery image'
            })
        }