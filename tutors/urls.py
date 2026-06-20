from django.urls import path

from . import views

urlpatterns = [
    path('apply/', views.tutor_apply, name='tutor_apply'),
    path('apply/success/', views.application_apply_success, name='application_apply_success'),
    path('admin/applications/', views.application_list, name='application_list'),
    path('admin/applications/<int:pk>/', views.application_detail, name='application_detail'),
    path('admin/applications/<int:pk>/activate/', views.approve_to_tutor, name='approve_to_tutor'),
    path('tutors/', views.tutor_list, name='tutor_list'),
    path('tutors/<int:pk>/', views.tutor_detail, name='tutor_detail'),
    path('tutors/<int:pk>/edit/', views.tutor_edit, name='tutor_edit'),
]
