from typing import Any

from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response

from nuvolar_airlines.airspace.serializers import FlightSerializer
from nuvolar_airlines.airspace.services import FlightService


class FlightViewSet(viewsets.ModelViewSet):
    service_class = FlightService
    serializer_class = FlightSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return self.service_class.get_flights()

    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        queryset = self.get_queryset()

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


