from django.contrib import admin
from .models import Airport, Aircraft, Flight


@admin.register(Airport)
class AirportAdmin(admin.ModelAdmin):
    list_display = ["name", "icao_code", "public_id"]


@admin.register(Aircraft)
class AircraftAdmin(admin.ModelAdmin):
    list_display = ["serial_number", "manufacturer"]


@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = ["aircraft", "departure_airport", "arrival_airport", "departure_time", "arrival_time"]
    list_filter = ["aircraft", "departure_airport", "arrival_airport", "departure_time", "arrival_time"]
    search_fields = ["aircraft", "departure_airport", "arrival_airport", "departure_time", "arrival_time"]

