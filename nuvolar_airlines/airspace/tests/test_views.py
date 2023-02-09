from django.urls import reverse
from rest_framework.test import APITestCase

from .factories import AircraftFactory, AirportFactory, FlightFactory


class TestFlightViewSet(APITestCase):
    def setUp(self) -> None:
        self.url = reverse("airspace:flights-list")
        self.dummy_flight = FlightFactory.create()
        self.detail_url = reverse(
            "airspace:flights-detail", kwargs={"public_id": self.dummy_flight.public_id}
        )
        self.aircraft = AircraftFactory.create()
        self.departure_airport = AirportFactory.create()
        self.arrival_airport = AirportFactory.create()
        self.payload = {
            "departure_airport": self.departure_airport.public_id,
            "arrival_airport": self.arrival_airport.public_id,
            "aircraft": self.aircraft.public_id,
            "departure_time": "2023-05-01 00:00:00",
            "arrival_time": "2023-05-02 00:00:00",
        }

    def test_flight_creation(self):
        response = self.client.post(self.url, self.payload, format="json")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.data["departure_airport"], self.departure_airport.__str__()
        )
        self.assertEqual(
            response.data["arrival_airport"], self.arrival_airport.__str__()
        )
        self.assertEqual(response.data["aircraft"], self.aircraft.__str__())

    def test_flight_creation_without_aircraft(self):
        self.payload.pop("aircraft")
        response = self.client.post(self.url, self.payload, format="json")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.data["departure_airport"], self.departure_airport.__str__()
        )
        self.assertEqual(
            response.data["arrival_airport"], self.arrival_airport.__str__()
        )
        self.assertEqual(response.data.get("aircraft", None), None)

    def test_flight_creation_with_invalid_aircraft(self):
        self.payload["aircraft"] = "invalid"
        response = self.client.post(self.url, self.payload, format="json")

        self.assertEqual(response.status_code, 400)

    def test_can_retrieve_flight_details(self):
        response = self.client.get(self.detail_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data["departure_airport"],
            self.dummy_flight.departure_airport.__str__(),
        )
        self.assertEqual(
            response.data["arrival_airport"],
            self.dummy_flight.arrival_airport.__str__(),
        )
        self.assertEqual(
            response.data["aircraft"], self.dummy_flight.aircraft.__str__()
        )

    def test_can_delete_flight(self):
        response = self.client.delete(self.detail_url)

        self.assertEqual(response.status_code, 204)

    def test_cannot_create_flight_with_past_departure_time(self):
        self.payload["departure_time"] = "2020-05-01 00:00:00"
        response = self.client.post(self.url, self.payload, format="json")

        self.assertEqual(response.status_code, 400)

    def test_cannot_create_flight_with_past_arrival_time(self):
        self.payload["arrival_time"] = "2020-05-01 00:00:00"
        response = self.client.post(self.url, self.payload, format="json")

        self.assertEqual(response.status_code, 400)

    def test_cannot_create_flight_with_departure_time_greater_than_arrival_time(self):
        self.payload["arrival_time"] = "2020-05-01 00:00:00"
        self.payload["departure_time"] = "2020-05-02 00:00:00"
        response = self.client.post(self.url, self.payload, format="json")

        self.assertEqual(response.status_code, 400)
