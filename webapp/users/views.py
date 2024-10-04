from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import CustomUserCreationForm


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Redirect to a success page or the home page
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})


def profile(request):
    return render(request, 'profile.html')