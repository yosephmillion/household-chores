from django.urls import path

from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path(
        "households/<int:household_id>/",
        views.dashboard,
        name="dashboard",
    ),
]