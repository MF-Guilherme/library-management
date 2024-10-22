from django.urls import path
from .views import CustomLoginView, SignUpView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),  # Usa o login customizado
    path('signup/', SignUpView.as_view(), name='signup'),
]
