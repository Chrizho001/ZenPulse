from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import FitnessBlog, Session
from unfold.admin import ModelAdmin




# --- Fitness Blog Admin ---
@admin.register(FitnessBlog)
class FitnessBlogAdmin(ModelAdmin):
    list_display = ('title', 'slug', 'author', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('title', 'content', 'author__email')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('-created_at',)


# --- Session Admin ---
@admin.register(Session)
class SessionAdmin(ModelAdmin):
    list_display = ('id', 'user', 'start_date', 'start_time')
    list_filter = ('start_date',)
    search_fields = ('user__email', 'description')
    ordering = ('-start_date',)
