import requests
import json
from .api_exceptions import SoSApiException


class AuthenticationApi:

    def __init__(self, user_agent, base_url, username=None, password=None, key=None):
        self.base_url = base_url
        self.username = username
        self.password = password
        self.key = key
        self.user_agent = user_agent

    def get_request_headers(self):
        headers = {
            "Content-Type": "application/vnd.api+json",
            "Accept": "application/vnd.api+json",
            "User-Agent": self.user_agent
        }
        return headers

    def login(self):
        url = f'{self.base_url}login'
        request_body = json.dumps(
            {
                "data": {
                    "type": None,
                    "attributes": {
                        "username": self.username,
                        "password": self.password
                    }
                }
            }
        )

        request_headers = self.get_request_headers()

        response = requests.post(url=url, data=request_body, headers=request_headers)
        if response.status_code == 200:
            data = response.json().get('data')
            token = data.get('token')
            secret = data.get('secret')
            return {"token": token, "secret": secret}

        else:
            if response.status_code in range(400, 600):
                error_response = response.json()
                error = error_response.get('errors')[0]
                msg = 'Error occurred'
                if error:
                    msg = f'Status:{error.get("status")}, {error.get("title")}, {error.get("detail")}'
                raise SoSApiException(msg)

    def login_key(self, key):
        url = f'{self.base_url}login_key'
        request_body = json.dumps(
            {
                "data": {
                    "type": None,
                    "attributes": {
                        "key": key
                    }
                }
            }
        )

        request_headers = self.get_request_headers()
        response = requests.post(url=url, data=request_body, headers=request_headers)
        if response.status_code == 200:
            data = response.json().get('data')
            token = data.get('token')
            secret = data.get('secret')
            return {"token": token, "secret": secret}

        else:
            if response.status_code in range(400, 600):
                error_response = response.json()
                error = error_response.get('errors')[0]
                msg = 'Error occurred'
                if error:
                    msg = f'Status:{error.get("status")}, {error.get("title")}, {error.get("detail")}'
                raise SoSApiException(msg)
