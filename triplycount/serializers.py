# trips/serializers.py

from rest_framework import serializers
from .models import Trip, Expense

class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = ['id', 'trip_text', 'created_date']

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ['id', 'trip', 'pub_date', 'amount']
