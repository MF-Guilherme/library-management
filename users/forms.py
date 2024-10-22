from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from .models import User, Address

class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'autofocus': True}))  # O Django usa 'username' como identificador


class EmailUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')
    cpf = forms.CharField(max_length=11, required=True, label='CPF')
    phone = forms.CharField(max_length=11, required=True, label='Telefone')
    
    # Campos do endereço (você pode ajustar conforme a sua necessidade)
    zip_code = forms.CharField(max_length=8, required=True, label='CEP')
    street = forms.CharField(max_length=255, required=True, label='Rua')
    number = forms.CharField(max_length=10, required=True, label='Número')
    neighborhood = forms.CharField(max_length=100, required=True, label='Bairro')
    city = forms.CharField(max_length=100, required=True, label='Cidade')
    state = forms.CharField(max_length=2, required=True, label='Estado')
    complement = forms.CharField(max_length=50, required=False, label='Complemento')

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2', 'cpf', 'phone', 'zip_code', 'street', 'number', 'neighborhood', 'city', 'state', 'complement')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.username = user.email  # Define o username como o email
        user.cpf = self.cleaned_data['cpf']
        user.phone = self.cleaned_data['phone']

        if commit:
            # Criar o endereço do usuário
            address = Address.objects.create(
                zip_code=self.cleaned_data['zip_code'],
                street=self.cleaned_data['street'],
                number=self.cleaned_data['number'],
                neighborhood=self.cleaned_data['neighborhood'],
                city=self.cleaned_data['city'],
                state=self.cleaned_data['state'],
                complement=self.cleaned_data.get('complement', '')
            )
            user.addres_id = address
            user.save()
        return user