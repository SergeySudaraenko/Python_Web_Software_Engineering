
from django import forms
from .models import Author, Quote, Tag

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name', 'bio']

class QuoteForm(forms.ModelForm):
    class Meta:
        model = Quote
        fields = ['text', 'author', 'tags']
