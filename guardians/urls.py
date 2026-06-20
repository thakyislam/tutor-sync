from django.urls import path

from . import views

urlpatterns = [
    # Admin guardian management
    path('admin/guardians/', views.guardian_list, name='guardian_list'),
    path('admin/guardians/add/', views.guardian_add, name='guardian_add'),
    path('admin/guardians/<int:pk>/', views.guardian_detail, name='guardian_detail_admin'),
    path('admin/guardians/<int:pk>/deactivate/', views.guardian_deactivate, name='guardian_deactivate'),
    # Guardian self-service: student management
    path('guardians/students/add/', views.student_add, name='student_add'),
    path('guardians/students/<int:pk>/edit/', views.student_edit, name='student_edit'),
]
