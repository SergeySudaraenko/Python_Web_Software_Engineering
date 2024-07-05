from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Author, Quote, Tag
from .forms import AuthorForm, QuoteForm
from quotes_project.quotes import models

def author_detail(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    quotes = Quote.objects.filter(author=author)
    paginator = Paginator(quotes, 10)
    page = request.GET.get('page')
    quotes = paginator.get_page(page)
    return render(request, 'author_detail.html', {'author': author, 'quotes': quotes})

@login_required
def add_author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('author-list')
    else:
        form = AuthorForm()
    return render(request, 'add_author.html', {'form': form})

@login_required
def add_quote(request):
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('quote-list')
    else:
        form = QuoteForm()
    return render(request, 'add_quote.html', {'form': form})

def quote_list(request):
    quotes = Quote.objects.all()
    paginator = Paginator(quotes, 10)
    page = request.GET.get('page')
    quotes = paginator.get_page(page)
    return render(request, 'quote_list.html', {'quotes': quotes})

def tag_search(request, tag_name):
    tag = get_object_or_404(Tag, name=tag_name)
    quotes = tag.quotes.all()
    paginator = Paginator(quotes, 10)
    page = request.GET.get('page')
    quotes = paginator.get_page(page)
    return render(request, 'tag_search.html', {'tag': tag, 'quotes': quotes})

def top_tags(request):
    tags = Tag.objects.annotate(num_quotes=models.Count('quotes')).order_by('-num_quotes')[:10]
    return render(request, 'top_tags.html', {'tags': tags})
