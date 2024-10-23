from django.urls import path
from . import views
from .views import  BookCreateView


app_name = 'library'

urlpatterns = [
    path('', views.home, name='home'),
    path('library/books/', views.get_books_info, name='books'),
    path('library/book_register/', BookCreateView.as_view(), name='book_register'),
]