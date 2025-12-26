from django.contrib import admin
from .models import Mission, Target

class TargetInline(admin.TabularInline):
    model = Target
    extra = 1

@admin.register(Mission)
class MissionAdmin(admin.ModelAdmin):
    list_display = ['id', 'cat', 'is_complete', 'created_at']
    list_filter = ['is_complete', 'created_at']
    inlines = [TargetInline]

@admin.register(Target)
class TargetAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'country', 'mission', 'is_complete']
    list_filter = ['is_complete', 'country']
    search_fields = ['name', 'country']