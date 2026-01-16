from django.shortcuts import render
from django.http import JsonResponse


# Create your views here.
def index(request):
    return render(request, "index.html")


def health_check(request):
    """Health check endpoint for Render and load balancers."""
    return JsonResponse({"status": "healthy", "service": "snapbuy-api"})