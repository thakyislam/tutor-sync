from django.contrib import admin
from .models import TutorRequest


@admin.register(TutorRequest)
class TutorRequestAdmin(admin.ModelAdmin):
    list_display = ('pk', 'status', 'guardian', 'subject', 'assigned_tutor', 'created_at')
    list_filter = ('status',)
    search_fields = ('guardian__user__first_name', 'guardian__user__email')
    raw_id_fields = ('guardian', 'student', 'assigned_tutor')
