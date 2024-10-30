from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, DetailView, DeleteView, UpdateView, ListView
from django.contrib import messages
from django.contrib.messages import constants
from django.urls import reverse_lazy
from django.utils import timezone
from django.db import transaction
from .models import Book, Loan
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


def add_to_cart(request, book_id):
    cart = request.session.get('loan_cart', [])
    if book_id not in cart:
        cart.append(book_id)
        request.session['loan_cart'] = cart
        messages.success(request, "Livro adicionado ao carrinho.")
    else:
        messages.warning(request, "Este livro já está no seu carrinho.")

    return redirect('library:book_detail', pk=book_id)

def view_cart(request):
    cart = request.session.get('loan_cart', [])
    books = Book.objects.filter(id__in=cart)
    return render(request, 'view_cart.html', {'books': books})

def remove_from_cart(request, book_id):
    cart = request.session.get('loan_cart', [])
    if book_id in cart:
        cart.remove(book_id)
        request.session['loan_cart'] = cart
        messages.success(request, "Livro removido do carrinho de empréstimo.")
    return redirect('library:view_cart')

from django.utils import timezone

def finalize_loan(request):
    loan_days = 7
    cart = request.session.get('loan_cart', [])
    if cart:
        for book_id in cart:
            Loan.objects.create(
                user=request.user,
                book_id=book_id,
                return_date=timezone.now() + timezone.timedelta(days=loan_days),  # prazo de devolução
            )
        request.session['loan_cart'] = []  # Limpa o carrinho após finalizar o empréstimo
        messages.success(request, "Empréstimo finalizado com sucesso!")
    else:
        messages.warning(request, "Seu carrinho de empréstimo está vazio.")
    
    return redirect('library:loans')


def my_loans(request):
    loans = Loan.objects.filter(user=request.user)
    print(loans[0].book.author)
    return render(request, 'loan_list.html', {'loans': loans})


