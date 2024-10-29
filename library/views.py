from django.views.generic import CreateView, DetailView, DeleteView, UpdateView
from django.views.generic.list import ListView
from django.contrib import messages
from django.contrib.messages import constants
from django.urls import reverse_lazy
from django.db import transaction
from .models import Book
from .forms import BookForm


class BookHomeListView(ListView):
    model = Book    
    template_name = 'home.html'


class BookAdminListView(ListView):
    model = Book    
    template_name = 'books.html'


class BookCreateView(CreateView):
    model = Book
    form_class = BookForm
    template_name = 'book_register.html'
    success_url = reverse_lazy('library:home')
    
    @transaction.atomic
    def form_valid(self, form):
        messages.add_message(self.request, constants.SUCCESS, 'Livro cadastrado com sucesso!')
        return super().form_valid(form)


class BookDetailView(DetailView):
    model = Book
    template_name = 'book_details.html'
    context_object_name = 'book'


class BookDeleteView(DeleteView):
    model = Book
    template_name = 'delete_book.html'
    success_url = reverse_lazy('library:books')
    
    @transaction.atomic
    def form_valid(self, form):
        messages.add_message(self.request, constants.SUCCESS, 'Livro deletado com sucesso!')
        return super().form_valid(form)
    
class BookUpdateView(UpdateView):
    model = Book
    form_class = BookForm
    template_name = 'book_update.html'

    def get_success_url(self):
        return reverse_lazy('library:book_detail', kwargs={'pk': self.object.pk})

    @transaction.atomic
    def form_valid(self, form):
        if self.request.POST.get('cover_image-clear'):
            # Limpa a imagem atual
            form.instance.cover_image.delete(save=True)  # Deletar o arquivo do sistema
            form.instance.cover_image = None  # Limpa o campo no modelo

        messages.add_message(self.request, constants.SUCCESS, 'Livro atualizado com sucesso!')
        return super().form_valid(form)

   
