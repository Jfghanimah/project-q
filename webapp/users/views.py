from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomUserChangeForm
from games.models import Game
from .models import GameList, Rating

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Redirect to home page or profile
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})


def profile(request):
    user_ratings = Rating.objects.filter(user=request.user)
    user_games = [rating.game for rating in user_ratings]
    return render(request, 'profile.html', {'user_games': user_games})


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = CustomUserChangeForm(instance=request.user)
    return render(request, 'edit_profile.html', {'form': form})