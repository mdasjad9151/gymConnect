from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Admin, GymOwner, Trainer, GymUser

class AdminRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = Admin
        fields = ['name', 'email', 'password']

    def save(self, commit=True):
        admin = super().save(commit=False)
        admin.set_password(self.cleaned_data["password"])
        if commit:
            admin.save()
        return admin

# GymOwnerForm
class GymOwnerRegistrationForm(forms.ModelForm):
    class Meta:
        model = GymOwner
        fields = [
            'email', 'password', 'gym_name', 'contact_no', 'address', 
            'city', 'state', 'profile_picture'
        ]
        widgets = {
            'password': forms.PasswordInput(),
        }

# TrainerForm
class TrainerRegistrationForm(forms.ModelForm):
    class Meta:
        model = Trainer
        fields = [
            'email', 'password', 'name',  'contact_no', 
            'address', 'city', 'state', 'profile_picture', 'certificate_image'
        ]
        widgets = {
            'password': forms.PasswordInput(),
        }

# GymUserForm
class GymUserRegistrationForm(forms.ModelForm):
    class Meta:
        model = GymUser
        fields = [
            'email', 'password', 'name', 'contact_no', 
            'address', 'city', 'state', 'profile_picture'
        ]
        widgets = {
            'password': forms.PasswordInput(),
        }

class CustomLoginForm(AuthenticationForm):
    username = forms.EmailField(label="Email")

















