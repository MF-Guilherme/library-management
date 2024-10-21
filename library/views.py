from django.shortcuts import render
from .models import Book


def home(request):
    if request.method == 'GET':
        books = Book.objects.all()
        return render(request, 'home.html', {'books': books})