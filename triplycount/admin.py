from django.contrib import admin

from .models import Trip, Expense

class ExpenseInline(admin.TabularInline):
    model = Expense
    extra = 3


class TripAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["trip_text"]}),
        ("Date information", {"fields": ["created_date"], "classes": ["collapse"]}),
    ]
    inlines = [ExpenseInline]
    list_display = ["trip_text", "created_date", "was_published_recently"]
    list_filter = ["created_date"]
    search_fields = ["trip_text"]

admin.site.register(Trip, TripAdmin)
admin.site.register(Expense)