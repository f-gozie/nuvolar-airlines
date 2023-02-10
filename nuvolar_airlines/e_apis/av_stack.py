from django.conf import settings

from .base import BaseService


class AviationStackAPI(BaseService):
    def __init__(self):
        super().__init__(base_url="http://api.aviationstack.com/v1")
        self.api_key = settings.AVIATION_STACK_API_KEY

    def fetch_airports(self, **kwargs):
        response = self._send_request(
            method="GET",
            path=f"airports?access_key={self.api_key}",
            params=kwargs,
        )
        return self._get_json_response(response=response)
