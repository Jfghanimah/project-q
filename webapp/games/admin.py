from django.contrib import admin

# Register your models here.
from .models import Game, Genre, Studio, Publisher, Distributor, Platform

admin.site.register(Game)
admin.site.register(Genre)
admin.site.register(Studio)
admin.site.register(Publisher)
admin.site.register(Distributor)
admin.site.register(Platform)