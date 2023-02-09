from rest_framework import serializers

from nuvolar_airlines.airspace.models import Flight


class FlightSerializer(serializers.ModelSerializer):
    departure_airport = serializers.UUIDField()
    arrival_airport = serializers.UUIDField()
    aircraft = serializers.UUIDField(source='aircraft.public_id', required=False)

    class Meta:
        model = Flight
        fields = '__all__'
