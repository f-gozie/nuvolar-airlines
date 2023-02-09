from datetime import datetime

from django.utils import timezone

from nuvolar_airlines.contrib import exceptions as airspace_exceptions


def validate_date(date: str, field: str):
    try:
        return datetime.fromisoformat(date)
    except ValueError:
        raise airspace_exceptions.InvalidDateFormat(field)


def convert_str_to_aware_datetime(str_date: str, field: str):
    validated_date = validate_date(str_date, field)
    return timezone.make_aware(validated_date, timezone.get_current_timezone())
