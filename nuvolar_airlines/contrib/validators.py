from django.utils import timezone
from rest_framework import serializers


class FutureDateValidator:
    def __init__(self, message=None):
        self.message = message

    def __call__(self, value):
        if value < timezone.now():
            raise serializers.ValidationError("Date must be in the future")
