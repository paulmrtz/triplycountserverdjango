import datetime

from django.db import models
from django.utils import timezone
from django.contrib import admin

class Trip(models.Model):
    trip_text = models.CharField(max_length=200)
    created_date = models.DateTimeField("date created")
    def __str__(self):
        return self.trip_text
    @admin.display(
        boolean=True,
        ordering="created_date",
        description="Created recently?",
    )

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.created_date <= now

class Expense(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    pub_date = models.DateTimeField("date published")
    amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    def __str__(self):
        return str(self.pub_date) + str(self.amount)