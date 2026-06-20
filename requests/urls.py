from django.urls import path

from . import views

urlpatterns = [
    path('requests/', views.request_list, name='request_list'),
    path('requests/new/', views.request_create, name='request_create'),
    path('requests/export/', views.request_export, name='request_export'),
    path('requests/<int:pk>/', views.request_detail, name='request_detail'),
    path('requests/<int:pk>/edit/', views.request_update, name='request_update'),
    path('requests/<int:pk>/cancel/', views.request_cancel, name='request_cancel'),
]
