from django.urls import path
from . import views

urlpatterns = [
    path('guardians/', views.guardian_list, name='guardian_list'),
]
