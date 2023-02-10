from django.urls import reverse
from rest_framework.test import APITestCase

from nuvolar_airlines.airspace.services import FlightService

from .factories import AircraftFactory, AirportFactory, FlightFactory


class TestFlightViewSet(APITestCase):
    def setUp(self) -> None:
        self.url = reverse("airspace:flights-list")
        self.dummy_flight = FlightFactory.create(departure_time="2021-05-01 00:00:00")
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

    def test_can_filter_flights_within_a_time_range(self):
        self.payload["departure_time"] = "2023-05-06 00:00:00"
        self.payload["arrival_time"] = "2023-05-07 00:00:00"
        self.client.post(self.url, self.payload, format="json")

        self.payload["departure_time"] = "2023-05-06 00:00:00"
        self.payload["arrival_time"] = "2023-05-07 00:00:00"
        self.client.post(self.url, self.payload, format="json")

        response = self.client.get(
            self.url, {"departure_time__gte": "2023-05-06 00:00:00"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)

    def test_can_filter_flights_by_departure_airport(self):
        self.payload["departure_airport"] = self.departure_airport.public_id
        self.client.post(self.url, self.payload, format="json")

        response = self.client.get(
            self.url, {"departure_airport": self.departure_airport.icao_code}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_can_filter_flights_by_arrival_airport(self):
        self.payload["arrival_airport"] = self.arrival_airport.public_id
        self.client.post(self.url, self.payload, format="json")

        response = self.client.get(
            self.url, {"arrival_airport": self.arrival_airport.icao_code}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_can_add_aircraft_to_flight(self):
        new_dummy_flight = FlightFactory.create(aircraft=None)
        aircraft_url = reverse(
            "airspace:flights-add-aircraft", args=[new_dummy_flight.public_id]
        )

        response = self.client.post(
            aircraft_url, {"aircraft": self.aircraft.public_id}, format="json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["aircraft"], self.aircraft.__str__())

    def test_can_generate_flight_report(self):
        flights = FlightFactory.create_batch(10)

        data = {
            "departure_time": flights[0].departure_time.strftime("%Y-%m-%d %H:%M:%S"),
            "arrival_time": flights[0].arrival_time.strftime("%Y-%m-%d %H:%M:%S"),
        }

        result = FlightService.generate_report(data)

        self.assertIsInstance(result, dict)
        self.assertIn(flights[0].departure_airport.name, result)
        self.assertEqual(result[flights[0].departure_airport.name]["no_of_flights"], 1)
        self.assertIn(
            flights[0].aircraft.serial_number,
            result[flights[0].departure_airport.name]["aircrafts"],
        )
        self.assertEqual(
            result[flights[0].departure_airport.name]["aircrafts"][
                flights[0].aircraft.serial_number
            ],
            (flights[0].arrival_time - flights[0].departure_time).total_seconds() / 60,
        )


class TestAircraftViewSet(APITestCase):
    def setUp(self) -> None:
        self.url = reverse("airspace:aircrafts-list")
        self.aircraft = AircraftFactory.create()
        self.detail_url = reverse(
            "airspace:aircrafts-detail", args=[self.aircraft.public_id]
        )
        self.payload = {
            "serial_number": "AB12",
            "manufacturer": "Boeing",
        }
        self.aircraft = AircraftFactory.create()

    def test_can_create_aircraft(self):
        response = self.client.post(self.url, self.payload, format="json")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["serial_number"], self.payload["serial_number"])
        self.assertEqual(response.data["manufacturer"], self.payload["manufacturer"])

    def test_can_retrieve_aircraft(self):
        aircraft = AircraftFactory.create()
        detail_url = reverse("airspace:aircrafts-detail", args=[aircraft.public_id])
        response = self.client.get(detail_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["serial_number"], aircraft.serial_number)
        self.assertEqual(response.data["manufacturer"], aircraft.manufacturer)

    def test_can_update_aircraft(self):
        self.payload["manufacturer"] = "Airbus"
        response = self.client.put(self.detail_url, self.payload, format="json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["serial_number"], self.payload["serial_number"])
        self.assertEqual(response.data["manufacturer"], self.payload["manufacturer"])

    def test_can_delete_aircraft(self):
        response = self.client.delete(self.detail_url)

        self.assertEqual(response.status_code, 204)
