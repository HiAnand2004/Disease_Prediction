from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.db import models
from django.utils.text import slugify

class UserManager(BaseUserManager):  # Add this class
    def create_superuser(self, email, full_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
            
        return self.create_user(email, full_name, password, **extra_fields)

    def create_user(self, email, full_name, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, full_name=full_name, **extra_fields)
        user.set_password(password)
        user.save()
        return user

class User(AbstractUser):
    # Custom fields
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=150)
    
    # Remove username requirements
    username = models.CharField(max_length=150, unique=True, blank=True)
    
    # Use email as login field
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    objects = UserManager()

    def save(self, *args, **kwargs):
        if not self.username:
            # Generate username from full_name (e.g. "John Doe" -> "johndoe")
            base_username = slugify(self.full_name.lower().replace(' ', ''))
            self.username = base_username
            # Handle duplicates
            counter = 1
            while User.objects.filter(username=self.username).exists():
                self.username = f"{base_username}{counter}"
                counter += 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email