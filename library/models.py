from django.db import models
from users.models import User
from django.conf import settings

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    year = models.CharField(max_length=4)
    genre = models.CharField(max_length=100)
    isbn = models.CharField(max_length=13, unique=True)
    avaible = models.BooleanField(default=True)
    cover_image = models.ImageField(upload_to='book_covers/', blank=True, null=True)
    def __str__(self):
        return  self.title

class Loan(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    loan_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateField()
    returned = models.BooleanField(default=False)
