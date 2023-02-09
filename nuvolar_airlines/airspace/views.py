from typing import Any

from django_filters import rest_framework as filters
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response

from nuvolar_airlines.airspace.filters import FlightFilterSet
from nuvolar_airlines.airspace.serializers import (
    AircraftAttachSerializer,
    AircraftSerializer,
    FlightSerializer,
)
from nuvolar_airlines.airspace.services import AircraftService, FlightService


class FlightViewSet(viewsets.ModelViewSet):
    lookup_field = "public_id"
    service_class = FlightService
    serializer_class = FlightSerializer
    permission_classes = [AllowAny]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = FlightFilterSet

    def get_queryset(self):
        return self.service_class.get_flights()

    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        response = self.serializer_class(queryset, many=True).data
        return Response(response, status=status.HTTP_200_OK)

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        obj = self.service_class.create_flight(serializer.validated_data)

        response = self.serializer_class(obj).data
        return Response(response, status=status.HTTP_201_CREATED)

    @action(
        detail=True, methods=["post"], url_path="add-aircraft", url_name="add-aircraft"
    )
    def add_aircraft(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer = AircraftAttachSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        obj = self.service_class.add_aircraft_to_flight(
            serializer.validated_data, flight_public_id=kwargs.get("public_id")
        )

        response = self.serializer_class(obj).data
        return Response(response, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=["get"],
        url_path="generate-report",
        url_name="generate-report",
    )
    def generate_report(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        query_params = request.GET

        report = self.service_class.generate_report(query_params)

        return Response(report, status=status.HTTP_200_OK)


class AircraftViewSet(viewsets.ModelViewSet):
    service_class = AircraftService
    serializer_class = AircraftSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return self.service_class.get_aircrafts()

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        obj = self.service_class.create_aircraft(serializer.validated_data)

        response = self.serializer_class(obj).data
        return Response(response, status=status.HTTP_201_CREATED)
