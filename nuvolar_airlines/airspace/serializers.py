from rest_framework import serializers

from nuvolar_airlines.airspace.models import Aircraft, Flight
from nuvolar_airlines.contrib.validators import FutureDateValidator


class FlightSerializer(serializers.ModelSerializer):
    departure_airport = serializers.UUIDField()
    arrival_airport = serializers.UUIDField()
    aircraft = serializers.UUIDField(required=False)
    departure_time = serializers.DateTimeField(validators=[FutureDateValidator()])
    arrival_time = serializers.DateTimeField(validators=[FutureDateValidator()])

    def validate(self, data):
        if data["departure_time"] == data["arrival_time"]:
            raise serializers.ValidationError(
                "Departure and arrival airports must be different"
            )
        if data["departure_time"] > data["arrival_time"]:
            raise serializers.ValidationError(
                "Departure time must be before arrival time"
            )
        return data

    class Meta:
        model = Flight
        fields = "__all__"


class AircraftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aircraft
        fields = "__all__"


class AircraftAttachSerializer(serializers.Serializer):
    aircraft = serializers.UUIDField()
