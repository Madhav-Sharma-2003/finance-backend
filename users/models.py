from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('analyst', 'Analyst'),
        ('viewer', 'Viewer'),
    ]

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default = 'viewer'
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.username} ({self.role})"