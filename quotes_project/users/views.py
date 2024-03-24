from django import forms
from django.contrib.auth import authenticate, login
from users.forms import UserCreationForm, QuoteForm, AuthorForm
from quotes.models import Quote, Author
from pymongo import MongoClient
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import QuoteForm, AuthorForm
from .decorators import user_authenticated


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user or not user.is_active:
                raise forms.ValidationError("Incorrect username or password")
        return self.cleaned_data
    

@user_authenticated
def add(request):
    if request.method == 'POST':
        quote_form = QuoteForm(request.POST)
        author_form = AuthorForm(request.POST)
        
        if quote_form.is_valid() and author_form.is_valid():
            quote_text = quote_form.cleaned_data['quote']
            author_name = author_form.cleaned_data['fullname']
            author, created = Author.objects.get_or_create(fullname=author_name)
            quote = Quote.objects.create(quote=quote_text, author=author)
            return redirect('/')
        
    else:
        quote_form = QuoteForm()
        author_form = AuthorForm()
        
    return render(request, 'add.html', {'quote_form': quote_form, 'author_form': author_form})