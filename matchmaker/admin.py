from django.contrib import admin

from .models import Musician, SoloAllRules, SoloRandom

# Register your models here.

admin.site.register(Musician)
admin.site.register(SoloAllRules)
admin.site.register(SoloRandom)