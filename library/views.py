from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import CreateView
from django.contrib import messages
from django.contrib.messages import constants
from django.urls import reverse_lazy
from django.db import transaction
from .models import Book
from .forms import BookForm


def home(request):
    if request.method == 'GET':
        books = Book.objects.all().order_by('-id')
        return render(request, 'home.html', {'books': books})
    
def get_books_info(request):
    if request.method == 'GET':
        books = Book.objects.all()
        return render(request, 'books.html', {'books': books})


class BookCreateView(CreateView):
    model = Book
    form_class = BookForm
    template_name = 'book_register.html'
    success_url = reverse_lazy('library:home')
    
    @transaction.atomic
    def form_valid(self, form):
        messages.add_message(self.request, constants.SUCCESS, 'Livro cadastrado com sucesso!')
        return super().form_valid(form)
