from uuid import UUID

from django.db.models import QuerySet
from django.utils import timezone

from nuvolar_airlines.contrib import exceptions as airspace_exceptions
from nuvolar_airlines.contrib.services import BaseService

from .models import Aircraft, Airport, Flight


class AirportService(BaseService):
    def __init__(self):
        super().__init__()
        self.model = Airport


class AircraftService(BaseService):
    def __init__(self):
        super().__init__()
        self.model = Aircraft

    @staticmethod
    def get_aircrafts() -> QuerySet[Aircraft]:
        return Aircraft.objects.all()

    @staticmethod
    def create_aircraft(data: dict):
        if Aircraft.objects.filter(data.get("icao_code")).exists():
            raise airspace_exceptions.AlreadyExists(Aircraft, data.get("icao_code"))
        return Aircraft.objects.create(**data)


class FlightService(BaseService):
    def __init__(self):
        super().__init__()
        self.model = Flight

    @staticmethod
    def get_flights() -> QuerySet[Flight]:
        return Flight.objects.all()

    @staticmethod
    def create_flight(data: dict):
        departure_airport = AirportService().get_obj_by_public_id(
            data.pop("departure_airport")
        )
        arrival_airport = AirportService().get_obj_by_public_id(
            data.pop("arrival_airport")
        )
        aircraft = AircraftService().get_obj_by_public_id(
            data.pop("aircraft", None), raise_exception=False
        )

        return Flight.objects.create(
            departure_airport=departure_airport,
            arrival_airport=arrival_airport,
            aircraft=aircraft,
            **data
        )

    @staticmethod
    def add_aircraft_to_flight(data: dict, flight_public_id: UUID):
        flight = FlightService().get_obj_by_public_id(flight_public_id)
        aircraft = AircraftService().get_obj_by_public_id(data.get("aircraft"))

        if flight.aircraft:
            raise airspace_exceptions.AlreadyHasRelationship(Flight.__name__, aircraft)
        if flight.departure_time < timezone.now():
            raise airspace_exceptions.FlightAlreadyDeparted()

        flight.aircraft = aircraft
        flight.save()
        return flight
