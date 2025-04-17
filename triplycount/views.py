from django.db.models import F
from django.shortcuts import get_object_or_404, render
from django.template import loader
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect
from .models import Trip, Expense

class IndexView(generic.ListView):
    template_name = "trips/index.html"
    context_object_name = "latest_trip_list"

    def get_queryset(self):
        return Trip.objects.filter(created_date__lte=timezone.now()).order_by("-created_date")

# def index(request):
#     latest_trip_list = Trip.objects.order_by("-created_date")
#     context = {"latest_trip_list": latest_trip_list}
#     return render(request, "trips/index.html", context)

class DetailView(generic.DetailView):
    model = Trip
    template_name = "trips/detail.html"

    def get_queryset(self):
        """
        Excludes any trips that aren't created yet.
        """
        return Trip.objects.filter(created_date__lte=timezone.now())

# def detail(request, trip_id):
#     trip = get_object_or_404(Trip, pk=trip_id)
#     return render(request, "trips/detail.html", {"trip": trip})

class ResultsView(generic.DetailView):
    model = Trip
    template_name = "trips/results.html"

def expenses(request, trip_id):
    response = "You're looking at the expenses of trip %s."
    return HttpResponse(response % trip_id)

# def totalexpenses(request, trip_id):
#     trip = Expense.objects.filter()
#     return HttpResponse(output)

def addexpenseplusone(request, trip_id):
    trip = get_object_or_404(Trip, pk=trip_id)
    try:
        selected_expense = trip.expense_set.get(pk=request.POST["expense"])
    except (KeyError, Expense.DoesNotExist):
        # Redisplay the trip voting form.
        return render(
            request,
            "trips/detail.html",
            {
                "trip": trip,
                "error_message": "You didn't select an expense.",
            },
        )
    else:
        selected_expense.amount = F("amount") + 1
        selected_expense.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("trips:results", args=(trip.id,)))
    