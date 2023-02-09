from uuid import UUID

from django.db.models import QuerySet

from .models import Airport, Aircraft, Flight
from nuvolar_airlines.airspace import exceptions as airspace_exceptions
from nuvolar_airlines.contrib.services import BaseService


class AirportService(BaseService):
    def __init__(self):
        super().__init__()
        self.model = Airport


class AircraftService(BaseService):
    def __init__(self):
        super().__init__()
        self.model = Aircraft


class FlightService(BaseService):
    def __init__(self):
        super().__init__()
        self.model = Flight

    @staticmethod
    def get_flights() -> QuerySet[Flight]:
        return Flight.objects.all()

    @staticmethod
    def create_flight(data: dict):
        departure_airport = AirportService().get_obj_by_public_id(data.pop('departure_airport'))
        arrival_airport = AirportService().get_obj_by_public_id(data.pop('arrival_airport'))
        aircraft = AircraftService().get_obj_by_public_id(data.pop('aircraft', None), raise_exception=False)

        return Flight.objects.create(
            departure_airport=departure_airport,
            arrival_airport=arrival_airport,
            aircraft=aircraft,
            **data
        )

