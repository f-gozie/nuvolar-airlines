from django.core.management import BaseCommand

from nuvolar_airlines.airspace.models import Airport
from nuvolar_airlines.e_apis.av_stack import AviationStackAPI


class Command(BaseCommand):
    def __init__(self):
        self.api = AviationStackAPI()
        super().__init__()

    def add_arguments(self, parser):
        parser.add_argument(
            "--limit",
            type=int,
            default=100,
            help="Number of airports to fetch from the API",
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Populating airports"))
        airports = self.api.fetch_airports(limit=options["limit"])

        airport_objs = [
            Airport(name=airport["airport_name"], icao_code=airport["icao_code"])
            for airport in airports["data"]
        ]

        Airport.objects.bulk_create(airport_objs, ignore_conflicts=True)

        self.stdout.write(self.style.SUCCESS("Successfully populated airports"))
