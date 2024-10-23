from django.urls import path
from . import  views

app_name = 'library'

urlpatterns = [
    path('', views.home, name='home'),
    path('library/books/', views.get_books_info, name='books'),
    path('library/book_register/', views.book_register, name='book_register'),
]