from django.urls import path
from rest_framework import routers

from . import views

app_name = "airspace"

routes = routers.SimpleRouter()

routes.register("flights", views.FlightViewSet, basename="flights")

urlpatterns = routes.urls
