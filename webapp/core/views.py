from django.shortcuts import render
from django.conf import settings

# Create your views here.

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def changelog(request):
    return render(request, 'changelog.html')

def latest_version(request):
    """
    Adds the application's latest version number to the template context.
    """
    return {'LATEST_VERSION': settings.LATEST_VERSION}