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
            'password': forms.PasswordInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 transition duration-200',
                'placeholder': 'Enter your password'
            }),
        }

    def __init__(self, *args, **kwargs):
        super(GymOwnerRegistrationForm, self).__init__(*args, **kwargs)
        
        # Add Tailwind CSS classes to all fields for consistent styling
        common_classes = 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 transition duration-200'
        
        # Apply the styles to each field
        for field in self.fields:
            if field != 'password':  # Password field already styled in widgets
                self.fields[field].widget.attrs.update({
                    'class': common_classes,
                    'placeholder': f'Enter your {field.replace("_", " ")}'
                })


# TrainerForm
class TrainerRegistrationForm(forms.ModelForm):
    class Meta:
        model = Trainer
        fields = [
            'email', 'password', 'name', 'contact_no', 
            'address', 'city', 'state', 'profile_picture', 'certificate_image'
        ]
        widgets = {
            'password': forms.PasswordInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 transition duration-200',
                'placeholder': 'Enter your password'
            }),
        }

    def __init__(self, *args, **kwargs):
        super(TrainerRegistrationForm, self).__init__(*args, **kwargs)
        
        # Common Tailwind CSS classes for form fields
        common_classes = 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 transition duration-200'
        
        # Apply Tailwind styles to each field
        for field in self.fields:
            if field != 'password':  # Password field already styled
                self.fields[field].widget.attrs.update({
                    'class': common_classes,
                    'placeholder': f'Enter your {field.replace("_", " ")}'
                })

# GymUserForm
class GymUserRegistrationForm(forms.ModelForm):
    class Meta:
        model = GymUser
        fields = [
            'email', 'password', 'name', 'contact_no', 
            'address', 'city', 'state', 'profile_picture'
        ]
        widgets = {
            'password': forms.PasswordInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 transition duration-200',
                'placeholder': 'Enter your password'
            }),
        }

    def __init__(self, *args, **kwargs):
        super(GymUserRegistrationForm, self).__init__(*args, **kwargs)
        
        # Common Tailwind CSS classes for form fields
        common_classes = 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 transition duration-200'
        
        # Apply Tailwind styles to each field
        for field in self.fields:
            if field != 'password':  # Password field already styled
                self.fields[field].widget.attrs.update({
                    'class': common_classes,
                    'placeholder': f'Enter your {field.replace("_", " ")}'
                })
class CustomLoginForm(AuthenticationForm):
    username = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 transition duration-200',
            'placeholder': 'Enter your email',
        })
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 transition duration-200',
            'placeholder': 'Enter your password',
        })
    )

















