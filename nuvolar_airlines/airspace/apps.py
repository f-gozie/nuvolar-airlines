from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AirSpaceConfig(AppConfig):
    name = "nuvolar_airlines.airspace"
    verbose_name = _("AirSpace")

    def ready(self):
        try:
            import nuvolar_airlines.airspace.signals  # noqa F401
        except ImportError:
            pass
