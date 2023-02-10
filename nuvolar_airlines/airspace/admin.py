from django.contrib import admin

from .models import Aircraft, Airport, Flight, FlightReport


@admin.register(Airport)
class AirportAdmin(admin.ModelAdmin):
    list_display = ["name", "icao_code", "public_id"]


@admin.register(Aircraft)
class AircraftAdmin(admin.ModelAdmin):
    list_display = ["serial_number", "public_id", "manufacturer"]


@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = [
        "public_id",
        "aircraft",
        "departure_airport",
        "arrival_airport",
        "departure_time",
        "arrival_time",
    ]
    list_filter = [
        "aircraft",
        "departure_airport",
        "arrival_airport",
        "departure_time",
        "arrival_time",
    ]
    search_fields = [
        "aircraft",
        "departure_airport",
        "arrival_airport",
        "departure_time",
        "arrival_time",
    ]


@admin.register(FlightReport)
class FlightReportAdmin(admin.ModelAdmin):
    list_display = ["report_date", "airport_name", "no_flights", "aircraft_stats"]
    list_filter = ["report_date", "airport_name", "no_flights"]
    search_fields = ["report_date", "airport_name"]
