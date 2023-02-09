from rest_framework import status
from rest_framework.exceptions import APIException


class DoesNotExist(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_code = "does_not_exist"

    def __init__(self, klass, public_id):
        self.detail = f"{klass} with public ID {public_id} does not exist"


class AlreadyExists(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_code = "already_exists"

    def __init__(self, klass, unique_key):
        self.detail = f"{klass} with unique identifier <{unique_key}> already exists"


class AlreadyHasRelationship(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_code = "already_has_relationship"

    def __init__(self, klass, unique_key):
        self.detail = f"This {klass.lower()} already has a relationship with a <{unique_key}> entity"


class FlightAlreadyDeparted(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = "flight_already_departed"
    default_detail = "The departure time for this flight has already passed"
