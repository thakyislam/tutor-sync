from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect, render

handler404 = 'config.views.handler404'
handler500 = 'config.views.handler500'


def home_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'home.html')


urlpatterns = [
    path('', home_view, name='home'),
    path('', include('accounts.urls')),
    path('', include('dashboard.urls')),
    path('', include('tutors.urls')),
    path('', include('guardians.urls')),
    path('', include('requests.urls')),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
