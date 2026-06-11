from django.contrib import admin
from .models import Subject


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'is_active')
    list_filter = ('is_active', 'category')
    search_fields = ('name', 'category')
    list_editable = ('is_active',)
