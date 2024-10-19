from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Address


class UserAdmin(BaseUserAdmin):
    # Campos que você quer exibir no formulário de criação/edição
    fieldsets = (
        (None, {'fields': ('first_name', 'last_name', 'email', 'password')}),
        ('Informações Pessoais', {'fields': ('cpf', 'phone', 'addres_id')}),
    )

    # Campos que você quer exibir na lista de usuários
    list_display = ('cpf', 'first_name', 'email', 'created_at')

    # Campos que serão utilizados na pesquisa
    search_fields = ('username', 'email', 'cpf', 'phone')

    # Campos que podem ser filtrados na lista
    list_filter = ('is_staff', 'is_superuser', 'groups')


# Registra a classe UserAdmin com o modelo User
admin.site.register(User, UserAdmin)
admin.site.register(Address)
