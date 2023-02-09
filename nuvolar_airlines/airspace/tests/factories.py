import factory
from factory.django import DjangoModelFactory

from nuvolar_airlines.airspace import models


class FlightFactory(DjangoModelFactory):
    departure_airport = factory.SubFactory(
        "nuvolar_airlines.airspace.tests.factories.AirportFactory"
    )
    arrival_airport = factory.SubFactory(
        "nuvolar_airlines.airspace.tests.factories.AirportFactory"
    )
    aircraft = factory.SubFactory(
        "nuvolar_airlines.airspace.tests.factories.AircraftFactory"
    )
    departure_time = factory.Faker("date_time")
    arrival_time = factory.Faker("date_time")

    class Meta:
        model = models.Flight


class AirportFactory(DjangoModelFactory):
    icao_code = factory.Faker("bothify", text="????")

    class Meta:
        model = models.Airport


class AircraftFactory(DjangoModelFactory):
    serial_number = factory.Faker("bothify", text="????")

    class Meta:
        model = models.Aircraft
