from django.urls import path

from . import views

app_name = "interactivepuzzle"

urlpatterns = [
    path("", views.index, name="index"),
    path("register/", views.register_request, name="register"),
    path("login/", views.login_request, name="login"),
    path("logout/", views.logout_request, name="logout"),
    path("instructions/", views.instructions, name="instructions"),
    path("question", views.fetchquestion, name="fetchquestion"),
    path("submission/<int:id>/", views.submission_request, name="submission"),
    path("leaderboard/", views.fetch_leaderboard, name="leaderboard"),
    path("analytics/", views.get_analytics, name="analytics")
]
