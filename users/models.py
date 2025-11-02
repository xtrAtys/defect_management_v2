from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('engineer', 'Инженер'),
        ('manager', 'Менеджер'),
        ('observer', 'Наблюдатель'),
        ('director', 'Руководитель'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='engineer')
    phone = models.CharField(max_length=20, blank=True)
    department = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.get_full_name()} ({self.get_role_display()})"