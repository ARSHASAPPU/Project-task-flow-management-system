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


from django.db import models
from .models import User  # if not already imported
from datetime import date

class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(default='No description')
    start_date = models.DateField(default=date.today)
    end_date = models.DateField(default=date.today)  
    team_members = models.ManyToManyField(User)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    PRIORITY_CHOICES = [
        ('High', 'High'),
        ('Medium', 'Medium'),
        ('Low', 'Low'),
    ]
    STATUS_CHOICES = [
        ('To Do', 'To Do'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(default='No description')

    deadline = models.DateField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

# models.py
