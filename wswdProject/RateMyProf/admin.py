from django.contrib import admin

from .models import  Rating, Professor, Module
# Register your models here.

#admin.site.register(User)
admin.site.register(Rating)
admin.site.register(Professor)
admin.site.register(Module)

