# forms.py
from django import forms
from accounts.models import Trainer

class TrainerSelectForm(forms.Form):
    trainer = forms.ModelChoiceField(
        queryset=Trainer.objects.all(),
        empty_label="Select Trainer",
        widget=forms.Select(attrs={"class": "form-select w-full p-2 border border-gray-300 rounded"}),
    )
