from django.urls import path

from . import views

urlpatterns = [
    path("translate", views.index, name="index"),
    path("", views.translate, name="translate"),
]
