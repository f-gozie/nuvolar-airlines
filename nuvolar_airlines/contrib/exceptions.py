from django.utils.translation import gettext as _
from rest_framework import status
from rest_framework.exceptions import APIException


class DoesNotExist(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_code = "does_not_exist"

    def __init__(self, klass, public_id):
        self.detail = f"{klass} with public ID {public_id} does not exist"
