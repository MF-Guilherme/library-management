from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views
from .views import  BookCreateView, BookDetailView, BookDeleteView, BookHomeListView, BookAdminListView, BookUpdateView


app_name = 'library'

urlpatterns = [
    path('', BookHomeListView.as_view(), name='home'),
    path('library/books/', BookAdminListView.as_view(), name='books'),
    path('library/book_register/', BookCreateView.as_view(), name='book_register'),
    path('library/book/<int:pk>/', BookDetailView.as_view(), name='book_detail'),
    path('library/book/delete/<int:pk>', BookDeleteView.as_view(), name='delete_book'),
    path('library/book/update/<int:pk>', BookUpdateView.as_view(), name='update_book'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
