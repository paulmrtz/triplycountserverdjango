# trips/api_urls.py

from django.urls import include, path
from rest_framework import routers
from . import views

restRouter = routers.DefaultRouter()
restRouter.register(r'trips', views.TripViewSet)
restRouter.register(r'expenses', views.ExpenseViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(restRouter.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]