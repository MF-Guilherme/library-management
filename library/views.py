from django.shortcuts import render, redirect
from django.views.generic import CreateView, DetailView, DeleteView, UpdateView, ListView
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.utils import timezone
from django.db import transaction
from django.db.models import Max
from .models import Book, Loan
from .forms import BookForm


class BookHomeListView(LoginRequiredMixin, ListView):
    model = Book    
    template_name = 'home.html'
    paginate_by = 12

    def get_queryset(self):
        return Book.objects.filter(avaible=True).order_by('title')


class BookAdminListView(UserPassesTestMixin, ListView):
    model = Book    
    template_name = 'books.html'
    login_url = reverse_lazy('login')
    raise_exception = False

    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        # Redireciona para a tela de login se o usuário não estiver autenticado
        if not self.request.user.is_authenticated:
            messages.warning(self.request, "Por favor, faça login como administrador para acessar esta página")
            return redirect(self.get_login_url())
        # Lança um erro 403 apenas se o usuário não for staff
        messages.warning(self.request, "Você não tem permissão para acessar esta página")
        return redirect('/')  # Aqui redireciona para a home ou outra página de sua preferência.
    
    def get_queryset(self):
        return Book.objects.order_by('-id')
  

class BookCreateView(UserPassesTestMixin, CreateView):
    model = Book
    form_class = BookForm
    template_name = 'book_register.html'
    success_url = reverse_lazy('library:books')
    
    def test_func(self):
        return self.request.user.is_staff
    
    def handle_no_permission(self):
    # Redireciona para a tela de login se o usuário não estiver autenticado
        if not self.request.user.is_authenticated:
            messages.warning(self.request, "Por favor, faça login como administrador para acessar esta página")
            return redirect(self.get_login_url())
        # Lança um erro 403 apenas se o usuário não for staff
        messages.warning(self.request, "Você não tem permissão para acessar esta página")
        return redirect('/')  # Aqui redireciona para a home ou outra página de sua preferência.
    
    @transaction.atomic
    def form_valid(self, form):
        messages.add_message(self.request, constants.SUCCESS, 'Livro cadastrado com sucesso!')
        return super().form_valid(form)    


class BookDetailView(LoginRequiredMixin, DetailView):
    model = Book
    template_name = 'book_details.html'
    context_object_name = 'book'


class BookDeleteView(UserPassesTestMixin, DeleteView):
    model = Book
    template_name = 'delete_book.html'
    success_url = reverse_lazy('library:books')

    def test_func(self):
        return self.request.user.is_staff
    
    def handle_no_permission(self):
    # Redireciona para a tela de login se o usuário não estiver autenticado
        if not self.request.user.is_authenticated:
            messages.warning(self.request, "Por favor, faça login como administrador para acessar esta página")
            return redirect(self.get_login_url())
        # Lança um erro 403 apenas se o usuário não for staff
        messages.warning(self.request, "Você não tem permissão para esta ação")
        return redirect('/')  # Aqui redireciona para a home ou outra página de sua preferência.
    
    @transaction.atomic
    def form_valid(self, form):
        messages.add_message(self.request, constants.SUCCESS, 'Livro deletado com sucesso!')
        return super().form_valid(form)
    
class BookUpdateView(UserPassesTestMixin, UpdateView):
    model = Book
    form_class = BookForm
    template_name = 'book_update.html'

    def test_func(self):
        return self.request.user.is_staff
    
    def handle_no_permission(self):
    # Redireciona para a tela de login se o usuário não estiver autenticado
        if not self.request.user.is_authenticated:
            messages.warning(self.request, "Por favor, faça login como administrador para acessar esta página")
            return redirect(self.get_login_url())
        # Lança um erro 403 apenas se o usuário não for staff
        messages.warning(self.request, "Você não tem permissão para esta ação")
        return redirect('/')  # Aqui redireciona para a home ou outra página de sua preferência.

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

@login_required
def add_to_cart(request, book_id):
    cart = request.session.get('loan_cart', [])
    if book_id not in cart:
        cart.append(book_id)
        request.session['loan_cart'] = cart
        messages.success(request, "Livro adicionado ao carrinho.")
    else:
        messages.warning(request, "Este livro já está no seu carrinho.")

    return redirect('library:book_detail', pk=book_id)

@login_required
def view_cart(request):
    cart = request.session.get('loan_cart', [])
    books = Book.objects.filter(id__in=cart)
    return render(request, 'view_cart.html', {'books': books})

@login_required
def remove_from_cart(request, book_id):
    cart = request.session.get('loan_cart', [])
    if book_id in cart:
        cart.remove(book_id)
        request.session['loan_cart'] = cart
        messages.success(request, "Livro removido do carrinho de empréstimo.")
    return redirect('library:view_cart')

from django.utils import timezone

@login_required
def finalize_loan(request):
    loan_days = 7
    cart = request.session.get('loan_cart', [])
    if cart:
        for book_id in cart:
            Loan.objects.create(
                user=request.user,
                book_id=book_id,
                return_date=timezone.now() + timezone.timedelta(days=loan_days),  # prazo de devolução
                returned=False
            )
            Book.objects.filter(id=book_id).update(avaible=False)
            
        request.session['loan_cart'] = []  # Limpa o carrinho após finalizar o empréstimo
        messages.success(request, "Empréstimo finalizado com sucesso!")
    else:
        messages.warning(request, "Seu carrinho de empréstimo está vazio.")
    
    return redirect('library:loans')

@login_required
def my_loans(request):
    loans = Loan.objects.filter(user=request.user).order_by('-loan_date')
    print(loans[0].book.author)
    return render(request, 'loan_list.html', {'loans': loans})


