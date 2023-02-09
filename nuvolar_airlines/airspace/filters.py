from django_filters import rest_framework as filters

from nuvolar_airlines.airspace import models


class FlightFilterSet(filters.FilterSet):
    departure_time = filters.DateTimeFromToRangeFilter()
    arrival_time = filters.DateTimeFromToRangeFilter()
    departure_airport = filters.CharFilter(field_name="departure_airport__icao_code")
    arrival_airport = filters.CharFilter(field_name="arrival_airport__icao_code")

    class Meta:
        model = models.Flight
        fields = [
            "departure_time",
            "arrival_time",
            "departure_airport",
            "arrival_airport",
        ]
