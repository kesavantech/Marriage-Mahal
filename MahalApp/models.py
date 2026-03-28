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
    is_active = models.BooleanField(default=True)


    objects = UserManager()
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'phone', 'address']

    def __str__(self):
        return self.username


class HomeSlider(models.Model):
    mahal_name=models.CharField(max_length=100, null=True, blank=True)
    bg_color=models.CharField(max_length=100, null=True, blank=True)
    font_color=models.CharField(max_length=100, null=True, blank=True)
    font_size=models.CharField(max_length=100, null=True, blank=True)

    font_choice = [
        ("Arial", "Arial"),
    ("Georgia", "Georgia"),
    ("Times New Roman", "Times New Roman"),
    ("Poppins", "Poppins"),
    ("Montserrat", "Montserrat"),
    ("Roboto", "Roboto"),
    ("Lato", "Lato"),
    ("Open Sans", "Open Sans"),
    ("Playfair Display", "Playfair Display"),

    ]
    font_family = models.CharField(max_length=100, choices=font_choice, default='Arial', null=True, blank=True)
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

class ContactMessage(models.Model):
    name    = models.CharField(max_length=100)
    email   = models.EmailField()
    phone   = models.CharField(max_length=15)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    hall_choices = (
        ("Normal", "Normal"),
        ("AC", "AC"),
    )
    hall_type = models.CharField(max_length=100, choices=hall_choices, default='Normal')

    event_choices = (
        ("Engagement", "Engagement"),
        ("Marriage", "Marriage"),
        ("Baby Shower", "Baby Shower"),
        ("Ear Piercing", "Ear Piercing"),
        ("Birthday", "Birthday"),
        ("Baby Shower", "Baby Shower"),
        ("Conference", "Conference"),
        ("Political Event", "Political Event"),
        ("School Event", "School Event"),
        ("Awareness Event", "Awareness Event"),
        ("Others", "Others"),
    )
    event_type = models.CharField(max_length=100, choices=event_choices, default='Engagement')
    event_date = models.DateField()
    guest_count = models.IntegerField(default=1)
    special_requests = models.TextField(blank=True, null=True)

    EVENT_PRICES = {
        "Engagement": 70000,
        "Marriage": 85000,
        "Ear Piercing": 60000,
        "Birthday": 35000,
        "Baby Shower": 40000,
        "Conference": 50000,
        "Political Event": 50000,
        "School Event": 30000,
        "Awareness Event": 30000,
        "Others": 25000,
    }
    AC_EXTRA = 10000

    status_choices = (
        ("Pending", "Pending"),
        ("Confirmed", "Confirmed"),
        ("Rejected", "Rejected"),
        ("Cancelled", "Cancelled"),
    )
    status = models.CharField(max_length=20, choices=status_choices, default='Pending')

    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    advance_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    advance_paid = models.BooleanField(default=False)
    payment_screenshot = models.ImageField(upload_to='payments/', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        base_price = self.EVENT_PRICES.get(self.event_type, 25000)
        if self.hall_type == "AC":
            base_price += self.AC_EXTRA
        self.total_amount = base_price
        self.advance_amount = round(base_price * 0.15, 2)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.event_type} on {self.event_date}"




    
