from django.shortcuts import render
from django.http import JsonResponse


# Create your views here.
def home(request):
    return render(request, "home.html")


def health_check(request):
    """Health check endpoint for Render and load balancers."""
    return JsonResponse({"status": "healthy", "service": "snapbuy-api"})