from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    cpf = models.CharField(max_length=11, unique=True)
    phone = models.CharField(max_length=11, unique=True)
    addres_id = models.ForeignKey('Address', on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions_set',
        blank=True
    )

    def __str__(self):
        return self.email

class Address(models.Model):
    zip_code = models.CharField(max_length=8)
    street = models.CharField(max_length=255)
    number = models.CharField(max_length=10)
    neighborhood = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2)
    complement = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

