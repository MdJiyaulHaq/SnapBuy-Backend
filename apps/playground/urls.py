from django.urls import path

from apps.playground import views

app_name = "playground"

urlpatterns = [path("hello/", views.SayHelloView.as_view())]
