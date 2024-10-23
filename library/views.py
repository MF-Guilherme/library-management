from django.shortcuts import render, redirect
from .models import Book
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.messages import constants


def home(request):
    if request.method == 'GET':
        books = Book.objects.all()
        return render(request, 'home.html', {'books': books})
    
def get_books_info(request):
    if request.method == 'GET':
        books = Book.objects.all()
        return render(request, 'books.html', {'books': books})

def book_register(request):
    if request.method == 'GET':
        return render(request, 'book_register.html')
    elif request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        year = request.POST.get('year')
        genre = request.POST.get('genre')
        isbn = request.POST.get('isbn')
        avaible = request.POST.get('book_avaible') == "on"
        cover_image = request.FILES.get('book_cover')
        synopsis = request.POST.get('synopsis')

        book = Book()
        book.title = title
        book.author = author
        book.year = year
        book.genre = genre
        book.isbn = isbn
        book.avaible = avaible
        book.cover_image = cover_image
        book.synopsis = synopsis

        book.save()
        messages.add_message(request, constants.SUCCESS, "Livro cadastrado com sucesso!")
        return redirect('/')
        