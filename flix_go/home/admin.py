from django.contrib import admin
from .models import Home

class homeAdmin(admin.ModelAdmin):
    list_display = ('title','genre','release_year','country','description','rating')
admin.site.register(Home,homeAdmin)
# Register your models here.
