from django.db import models
from django.utils.translation import gettext_lazy as _

from nuvolar_airlines.contrib.models import BaseModel


class Aircraft(BaseModel):
    serial_number = models.CharField(max_length=255, unique=True)
    manufacturer = models.CharField(max_length=255)

    class Meta:
        verbose_name = _("Aircraft")
        verbose_name_plural = _("Aircrafts")

    def __str__(self):
        return f"Aircraft with serial number {self.serial_number}. Manufactured by {self.manufacturer}"


class Airport(BaseModel):
    name = models.CharField(max_length=255)
    icao_code = models.CharField(max_length=4, unique=True)

    class Meta:
        verbose_name = _("Airport")
        verbose_name_plural = _("Airports")

    def __str__(self):
        return f"Airport - {self.icao_code}"


class Flight(BaseModel):
    aircraft = models.ForeignKey(
        Aircraft, on_delete=models.CASCADE, null=True, blank=True
    )
    departure_airport = models.ForeignKey(
        Airport, on_delete=models.CASCADE, related_name="departure_airport"
    )
    arrival_airport = models.ForeignKey(
        Airport, on_delete=models.CASCADE, related_name="arrival_airport"
    )
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()

    class Meta:
        verbose_name = _("Flight")
        verbose_name_plural = _("Flights")

    def __str__(self):
        return f"Flight from {self.departure_airport} to {self.arrival_airport} at {self.departure_time}"
