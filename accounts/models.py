from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

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
    
    objects = BaseUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

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
    gym_name = models.CharField(max_length=255)
    address = models.TextField()

    def __str__(self):
        return f"GymOwner: {self.gym_name} - {self.email}"

# Trainer class
class Trainer(BaseUser):
    name = models.CharField(max_length=255)
    gym_id = models.ForeignKey(GymOwner, on_delete=models.CASCADE,  blank= True)

    def __str__(self):
        return f"Trainer: {self.name} - {self.email}"

# GymUser class
class GymUser(BaseUser):
    name = models.CharField(max_length=255)
    trainer_id = models.ForeignKey(Trainer, on_delete=models.CASCADE, blank=True, null=True)
    gym_id = models.ForeignKey(GymOwner, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"GymUser: {self.name} - {self.email}"