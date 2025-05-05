from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.apps import apps

# Custom user manager
class BaseUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

# BaseUser class
class BaseUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    # contact = models.CharField(max_length=15, blank=True, null=True)

    objects = BaseUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):
        # Check if password is set and needs hashing
        if self.password and not self.password.startswith('pbkdf2_sha256$') and not self.password.startswith('argon2$'):
            self.set_password(self.password)  # Hash the password
        super().save(*args, **kwargs)  # Call the real save method

    def __str__(self):
        return self.email


# Admin class inheriting from BaseUser
class Admin(BaseUser):
    name = models.CharField(max_length=50, blank=True)

    class Meta:
        verbose_name = 'Admin'
        verbose_name_plural = 'Admins'

    def save(self, *args, **kwargs):
        self.is_staff = True
        self.is_superuser = True
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Admin: {self.name} ({self.email})"

# GymOwner class
class GymOwner(BaseUser):
    name = models.CharField(max_length=255)
    contact_no = models.CharField(max_length=10, null= True)
    address = models.CharField(max_length=255,blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    

    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    def __str__(self):
        return f"GymOwner: {self.gym_name} - {self.email}"

# Trainer class
class Trainer(BaseUser):
    # Callable function for setting the default GymOwner
    def default_gym_owner():
        # Access GymOwner model after app is ready
        # GymOwner = apps.get_model('gymowner', 'GymOwner')  # Get the GymOwner model dynamically
        try:
            # Return the id of the default GymOwner
            return Trainer.objects.get(email="default@gymconnect.com").id
        except Trainer.DoesNotExist:
            # If the default GymOwner doesn't exist, return None or a valid default ID
            return None  # or a default valid ID if you prefer

    name = models.CharField(max_length=255)
    gym_id = models.ForeignKey(GymOwner, on_delete=models.CASCADE, blank=True, null=True, default=default_gym_owner)  # Using callable for default
    contact_no = models.CharField(max_length=10, null= True)
    address = models.CharField(max_length=255,blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)

    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    certificate_image = models.ImageField(upload_to='certificates/', blank=True, null=True)

    def __str__(self):
        return f"Trainer: {self.name} - {self.email}"

# GymUser class
class GymUser(BaseUser):
    def default_trainer():
        try:
            return GymOwner.objects.get(email="defaulttrainer@gymconnect.com").id
        except GymOwner.DoesNotExist:
            return None  # or a default valid ID if you prefer

    def default_gym_owner():

        try:
            return Trainer.objects.get(email="default@gymconnect.com").id
        except Trainer.DoesNotExist:
            return None 
    name = models.CharField(max_length=255)
    contact_no = models.CharField(max_length=10, null= True)
    trainer_id = models.ForeignKey(Trainer, on_delete=models.CASCADE, blank=True, null=True, default=default_trainer)
    gym_id = models.ForeignKey(GymOwner, on_delete=models.CASCADE, blank=True, null=True, default=default_gym_owner)
    address = models.CharField(max_length=255,blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)

    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    def __str__(self):
        return f"GymUser: {self.name} - {self.email}"

