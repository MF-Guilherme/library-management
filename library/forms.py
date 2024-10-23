from django import forms
from .models import Book
from datetime import datetime

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'genre', 'year', 'isbn', 'cover_image', 'synopsis', 'avaible']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'id': 'book_title'}),
            'author': forms.TextInput(attrs={'class': 'form-control', 'id': 'book_author'}),
            'genre': forms.TextInput(attrs={'class': 'form-control', 'id': 'book_genre'}),
            'year': forms.TextInput(attrs={'class': 'form-control', 'id': 'book_year'}),
            'isbn': forms.TextInput(attrs={'class': 'form-control', 'id': 'book_isbn'}),
            'cover_image': forms.ClearableFileInput(attrs={'class': 'form-control', 'id': 'book_cover'}),
            'synopsis': forms.Textarea(attrs={'class': 'form-control', 'aria-label': 'With textarea'}),
            'avaible': forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'book_avaible'}),
        }

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if title.isnumeric():
            raise forms.ValidationError("O título não pode conter apenas números.")
        return title

    def clean_author(self):
        author = self.cleaned_data.get('author')
        if author.isnumeric():
            raise forms.ValidationError("O nome do autor não pode conter apenas números.")
        return author

    def clean_year(self):
        year = self.cleaned_data.get('year')
        current_year = datetime.now().year
        if not year.isnumeric():
            raise forms.ValidationError("O ano de publicação deve conter apenas números.")
        if int(year) > current_year:
            raise forms.ValidationError("O ano de publicação não pode ser maior que o ano atual.")
        if len(str(year)) < 3:
            raise forms.ValidationError("O ano de publicação deve conter pelo menos 3 dígitos.")
        return year

    def clean_isbn(self):
        isbn = self.cleaned_data.get('isbn')
        if not isbn.isnumeric():
            raise forms.ValidationError("O código ISBN deve conter apenas números.")
        if Book.objects.filter(isbn=isbn).exists():
            raise forms.ValidationError("Este ISBN já está cadastrado para outro livro.")
        return isbn
    
    def clean_genre(self):
        genre = self.cleaned_data.get('genre')
        if genre.isnumeric():
            raise forms.ValidationError("O gênero literário não deve conter apenas números.")
        return genre

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        author = cleaned_data.get('author')
        genre = cleaned_data.get('genre')

        # Valida campos vazios
        if not title or not author or not genre:
            raise forms.ValidationError("Todos os campos devem ser preenchidos.")
        return cleaned_data
