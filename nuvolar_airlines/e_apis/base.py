from typing import Any

import environ
import requests

env = environ.Env()


class BaseService:
    def __init__(self, *, authorization: tuple = None, base_url: str):
        """
        - Initialize the base service
        - Set the base url and headers
        """
        self.base_url = base_url
        self.headers = self.__build_headers(authorization=authorization)

    def __build_headers(self, authorization: tuple = None) -> dict:
        """
        - Build the headers
        - Return the headers
        """
        if authorization:
            return {
                "Authorization": f"{authorization[0]} {authorization[1]}",
                "Content-Type": "application/json",
            }
        return {"Content-Type": "application/json"}

    def _send_request(self, method: str, path: str, **kwargs) -> Any:
        """
        - Send a request to the server
        - Return the response
        """
        url = f"{self.base_url}/{path}"
        response = requests.request(
            method=method,
            url=url,
            headers=self.headers,
            **kwargs,
        )
        return response

    def _get_json_response(self, response: Any) -> Any:
        """
        - Get the json response
        - Return the json response
        """
        return response.json()
