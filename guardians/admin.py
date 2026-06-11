from django.contrib import admin
from .models import GuardianProfile, Student


class StudentInline(admin.TabularInline):
    model = Student
    extra = 1
    fields = ('name', 'grade', 'notes')


@admin.register(GuardianProfile)
class GuardianProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'preferred_mode', 'created_at')
    search_fields = ('user__first_name', 'user__last_name', 'user__email')
    inlines = [StudentInline]


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'guardian', 'grade')
    search_fields = ('name', 'guardian__user__first_name')
