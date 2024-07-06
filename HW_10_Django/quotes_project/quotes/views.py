from pyexpat import model
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Author, Quote, Tag
from .forms import AuthorForm, QuoteForm
from .scraper import scrape_quotes


@login_required
def scrape_data(request):
    scrape_quotes()
    return redirect('index')


def index(request):
    quotes = Quote.objects.all()
    tags = Tag.objects.annotate(num_quotes=model.Count('quotes')).order_by('-num_quotes')[:10]
    return render(request, 'quotes/index.html', {'quotes': quotes, 'tags': tags})

def author_detail(request, author_id):
    author = get_object_or_404(Author, id=author_id)
    quotes = Quote.objects.filter(author=author)
    return render(request, 'quotes/author_detail.html', {'author': author, 'quotes': quotes})

@login_required
def add_author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = AuthorForm()
    return render(request, 'quotes/add_author.html', {'form': form})

@login_required
def add_quote(request):
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            quote = form.save(commit=False)
            quote.user = request.user
            quote.save()
            form.save_m2m()
            return redirect('index')
    else:
        form = QuoteForm()
    return render(request, 'quotes/add_quote.html', {'form': form})

def tag_quotes(request, tag_name):
    tag = get_object_or_404(Tag, name=tag_name)
    quotes = Quote.objects.filter(tags=tag)
    return render(request, 'quotes/tag_quotes.html', {'tag': tag, 'quotes': quotes})
