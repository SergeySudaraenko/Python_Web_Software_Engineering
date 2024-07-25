
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import AuthorForm





@login_required
def add_author(request):
    if request.method == "POST":
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = AuthorForm()
    return render(request, 'authors/add_author.html', {'form': form})
