from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def tutor_list(request):
    return render(request, 'coming_soon.html', {'page_title': 'Tutors'})


@login_required
def application_list(request):
    return render(request, 'coming_soon.html', {'page_title': 'Applications'})
