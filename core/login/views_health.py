# core/login/views_health.py
from django.http import HttpResponse

def health_check_view(request):
    return HttpResponse("OK", status=200)
