from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views
from .views import  BookCreateView, BookDetailView, BookDeleteView


app_name = 'library'

urlpatterns = [
    path('', views.home, name='home'),
    path('library/books/', views.get_books_info, name='books'),
    path('library/book_register/', BookCreateView.as_view(), name='book_register'),
    path('library/book/<int:pk>/', BookDetailView.as_view(), name='book_detail'),
    path('library/book/<int:pk>/delete/', BookDeleteView.as_view(), name='delete_book'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
