# models.py

from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('role', 'admin')
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, email, password, **extra_fields)

    def create_user(self, username, email, password=None, **extra_fields):
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractUser):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=100, unique=True)

    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('client', 'Client'),
    )

    phone = models.CharField(max_length=15, unique=True)
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='client'
    )
    address = models.CharField(max_length=255, blank=True)
    profile = models.FileField(upload_to="profile/", blank=True, null=True)


    objects = UserManager()
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username


class HomeSlider(models.Model):
    mahal_name=models.CharField(max_length=100, null=True, blank=True)
    bg_color=models.CharField(max_length=100, null=True, blank=True)
    font_color=models.CharField(max_length=100, null=True, blank=True)
    font_size=models.CharField(max_length=100, null=True, blank=True)
    logo=models.FileField(upload_to="logo/",null=True, blank=True)
    logo_radius=models.IntegerField(default=40)
    whatsapp_no=models.CharField(max_length=100, null=True, blank=True)
    phone=models.CharField(max_length=100, null=True, blank=True)
    gmail=models.EmailField(max_length=100, unique=True, null=True, blank=True)

    def __str__(self):
        return self.mahal_name


class HomeBanner(models.Model):
    image=models.ImageField(upload_to="home_banners/")
    title=models.CharField(max_length=100, blank=True, null=True)
    subtitle=models.CharField(max_length=100, blank=True, null=True)


    def __str__(self):
        return f"Banner {self.id}"

