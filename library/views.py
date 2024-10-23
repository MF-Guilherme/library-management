from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.messages import constants
from .models import Book
from .forms import BookForm


def home(request):
    if request.method == 'GET':
        books = Book.objects.all()
        return render(request, 'home.html', {'books': books})
    
def get_books_info(request):
    if request.method == 'GET':
        books = Book.objects.all()
        return render(request, 'books.html', {'books': books})

def book_register(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Livro cadastrado com sucesso!')
            return redirect('/')
        else:
            messages.error(request, 'Erro ao cadastrar o livro. Verifique os campos.')
    else:
        form = BookForm()

    return render(request, 'book_register.html', {'form': form})
        