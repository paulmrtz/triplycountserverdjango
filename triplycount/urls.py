from django.urls import path

from . import views

app_name = "trips"
urlpatterns = [
    # ex: /triplycount/trips/
    path("trips/", views.IndexView.as_view(), name="index"),
    # ex: /triplycount/trips/5/
    path("trips/<int:pk>/", views.DetailView.as_view(), name="detail"),
    # ex: /triplycount/trips/5/expenses/
    path("trips/<int:trip_id>/expenses/", views.expenses, name="expenses"),
    # ex: /triplycount/trips/5/addexpenseplusone/
    path("trips/<int:trip_id>/addexpenseplusone/", views.addexpenseplusone, name="addexpenseplusone"),
    path("trips/<int:pk>/results/", views.ResultsView.as_view(), name="results"),
]