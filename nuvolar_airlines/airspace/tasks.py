from django.utils import timezone

from config import celery_app
from nuvolar_airlines.airspace.models import FlightReport


@celery_app.task()
def store_flight_report(analysis: dict):
    for airport, data in analysis.items():
        FlightReport.objects.create(
            report_date=timezone.now(),
            airport_name=airport,
            no_flights=data.get("no_of_flights"),
            aircraft_stats=data.get("aircrafts"),
        )
