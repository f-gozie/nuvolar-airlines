from rest_framework import routers

from . import views

app_name = "airspace"

routes = routers.SimpleRouter()

routes.register("flights", views.FlightViewSet, basename="flights")
routes.register("aircrafts", views.AircraftViewSet, basename="aircrafts")

urlpatterns = routes.urls
