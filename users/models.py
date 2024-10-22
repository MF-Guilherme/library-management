from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, cpf, first_name, last_name, password=None, **extra_fields):
        if not email:
            raise ValueError('O endereço de e-mail deve ser fornecido')
        email = self.normalize_email(email)
        user = self.model(email=email, cpf=cpf, first_name=first_name, last_name=last_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, cpf, first_name, last_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser precisa ter is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser precisa ter is_superuser=True.')

        return self.create_user(email, cpf, first_name, last_name, password, **extra_fields)


class User(AbstractUser):
    email = models.EmailField(unique=True)  # Torna o campo de e-mail obrigatório e único
    username = None  # Remove o campo username para não ser utilizado

    cpf = models.CharField(max_length=11, unique=True)
    phone = models.CharField(max_length=11, unique=True)
    addres_id = models.ForeignKey('Address', on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'  # Define o campo email como identificador para login
    REQUIRED_FIELDS = ['cpf', 'first_name', 'last_name']  # Remove username da lista de campos obrigatórios

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


