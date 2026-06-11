from django.contrib import admin
from .models import TutorProfile, TutorApplication


class SubjectInline(admin.TabularInline):
    model = TutorProfile.subjects.through
    extra = 1
    verbose_name = 'Subject'
    verbose_name_plural = 'Subjects'


@admin.register(TutorProfile)
class TutorProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'verified', 'experience_yrs', 'hourly_rate', 'created_at')
    list_filter = ('status', 'verified')
    search_fields = ('user__first_name', 'user__last_name', 'user__email')
    inlines = [SubjectInline]
    exclude = ('subjects',)


@admin.register(TutorApplication)
class TutorApplicationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'status', 'reviewed_by', 'submitted_at')
    list_filter = ('status',)
    search_fields = ('full_name', 'email')
