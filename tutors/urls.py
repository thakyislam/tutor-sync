from django.urls import path
from . import views

urlpatterns = [
    path('tutors/', views.tutor_list, name='tutor_list'),
    path('admin/applications/', views.application_list, name='application_list'),
]
