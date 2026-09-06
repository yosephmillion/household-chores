from django.urls import path

from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path(
        "households/<int:household_id>/",
        views.dashboard,
        name="dashboard",
    ),
    path(
        "chores/<int:chore_id>/complete/",
        views.complete_chore,
        name="complete_chore",
    ),
    path(
    "households/<int:household_id>/calendar/",
    views.calendar,
    name="calendar",
    ),
]