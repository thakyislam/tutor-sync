from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_view, name='profile'),
    path('notifications/', views.notification_list_view, name='notifications'),
    path('password/change/', views.password_change_view, name='password_change'),
    # Admin user management
    path('admin/users/', views.admin_user_list, name='admin_user_list'),
    path('admin/users/add/', views.admin_user_create, name='admin_user_create'),
    path('admin/users/<int:pk>/edit/', views.admin_user_edit, name='admin_user_edit'),
]
