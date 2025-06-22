from django.db import models

# Create your models here.


class AdminUser(models.Model):
    username = models.CharField(
        max_length=150,
        unique=True,
        default='admin'
    )
    password = models.CharField(
        max_length=128,
        default='admin123'  # Insecure; use hashed in real apps
    )
    secret_code = models.CharField(
        max_length=6,
        default='000000',
        help_text='6-digit admin secret code'
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.username
    
from django.db import models

class User(models.Model):
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Team Member', 'Team Member'),
    ]

    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  # For real use: hash this
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    joined_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name

