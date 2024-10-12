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

class GymOwnerRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = GymOwner
        fields = ['gym_name', 'email', 'password', 'address']

    def save(self, commit=True):
        owner = super().save(commit=False)
        owner.set_password(self.cleaned_data["password"])
        if commit:
            owner.save()
        return owner

class TrainerRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = Trainer
        fields = ['name', 'email', 'password', 'gym_id']

    def save(self, commit=True):
        trainer = super().save(commit=False)
        trainer.set_password(self.cleaned_data["password"])
        if commit:
            trainer.save()
        return trainer

class GymUserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = GymUser
        fields = ['name', 'email', 'password', 'trainer_id']

    def save(self, commit=True):
        gym_user = super().save(commit=False)
        gym_user.set_password(self.cleaned_data["password"])
        if commit:
            gym_user.save()
        return gym_user

class CustomLoginForm(AuthenticationForm):
    username = forms.EmailField(label="Email")
















# from django import forms
# from .models import Admin

# class AdminForm(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput())  # Render password field with password input

#     class Meta:
#         model = Admin
#         fields = ['name', 'email', 'password']  # Specify the fields you want in the form

#     def save(self, commit=True):
#         admin = super().save(commit=False)
#         admin.set_password(self.cleaned_data["password"])  # Hash the password before saving
#         if commit:
#             admin.save()
#         return admin
