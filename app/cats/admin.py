from django.contrib import admin
from .models import SpyCat

@admin.register(SpyCat)
class SpyCatAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'breed', 'years_of_experience', 'salary', 'created_at']
    search_fields = ['name', 'breed']
    list_filter = ['breed', 'created_at']