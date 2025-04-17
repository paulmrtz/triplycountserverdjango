import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Trip


class TripModelTests(TestCase):
    def test_was_published_recently_with_future_trip(self):
        """
        was_published_recently() returns False for trips whose created_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_trip = Trip(created_date=time)
        self.assertIs(future_trip.was_published_recently(), False)

    def test_was_published_recently_with_old_trip(self):
        """
        was_published_recently() returns False for trips whose created_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_trip = Trip(created_date=time)
        self.assertIs(old_trip.was_published_recently(), False)


    def test_was_published_recently_with_recent_trip(self):
        """
        was_published_recently() returns True for trips whose created_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_trip = Trip(created_date=time)
        self.assertIs(recent_trip.was_published_recently(), True)

def create_trip(trip_text, days):
    """
    Create a trip with the given `trip_text` and published the
    given number of `days` offset to now (negative for trips published
    in the past, positive for trips that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Trip.objects.create(trip_text=trip_text, created_date=time)


class TripIndexViewTests(TestCase):
    def test_no_trips(self):
        """
        If no trips exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse("trips:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No trips are available.")
        self.assertQuerySetEqual(response.context["latest_trip_list"], [])

    def test_past_trip(self):
        """
        Trips with a created_date in the past are displayed on the
        index page.
        """
        trip = create_trip(trip_text="Past trip.", days=-30)
        response = self.client.get(reverse("trips:index"))
        self.assertQuerySetEqual(
            response.context["latest_trip_list"],
            [trip],
        )

    def test_future_trip(self):
        """
        Trips with a created_date in the future aren't displayed on
        the index page.
        """
        create_trip(trip_text="Future trip.", days=30)
        response = self.client.get(reverse("trips:index"))
        self.assertContains(response, "No trips are available.")
        self.assertQuerySetEqual(response.context["latest_trip_list"], [])

    def test_future_trip_and_past_trip(self):
        """
        Even if both past and future trips exist, only past trips
        are displayed.
        """
        trip = create_trip(trip_text="Past trip.", days=-30)
        create_trip(trip_text="Future trip.", days=30)
        response = self.client.get(reverse("trips:index"))
        self.assertQuerySetEqual(
            response.context["latest_trip_list"],
            [trip],
        )

    def test_two_past_trips(self):
        """
        The trips index page may display multiple trips.
        """
        trip1 = create_trip(trip_text="Past trip 1.", days=-30)
        trip2 = create_trip(trip_text="Past trip 2.", days=-5)
        response = self.client.get(reverse("trips:index"))
        self.assertQuerySetEqual(
            response.context["latest_trip_list"],
            [trip2, trip1],
        )

class TripDetailViewTests(TestCase):
    def test_future_trip(self):
        """
        The detail view of a trip with a created_date in the future
        returns a 404 not found.
        """
        future_trip = create_trip(trip_text="Future trip.", days=5)
        url = reverse("trips:detail", args=(future_trip.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_trip(self):
        """
        The detail view of a trip with a created_date in the past
        displays the trip's text.
        """
        past_trip = create_trip(trip_text="Past Trip.", days=-5)
        url = reverse("trips:detail", args=(past_trip.id,))
        response = self.client.get(url)
        self.assertContains(response, past_trip.trip_text)