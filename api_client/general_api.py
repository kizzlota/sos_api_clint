import hmac
import hashlib
import requests
from .api_exceptions import SoSApiException


class GeneralApiEndpoints:

    def __init__(self, token, secret, base_url, user_agent):
        self.token = token
        self.secret = secret
        self.signature = None
        self.base_url = base_url
        self.user_agent = user_agent

    def calculate_signature(self, body):
        signature = hmac.new(
            self.secret.encode('utf-8'),
            body.encode('utf-8'),
            hashlib.sha256).hexdigest()
        return signature

    def get_headers(self):
        headers = {
            "Authorization": f"SOS-SIGV1 {self.token};{self.signature}",
            "Content-Type": "application/vnd.api+json",
            "Accept": "application/vnd.api+json",
            "User-Agent": self.user_agent
        }
        return headers

    def me(self, body):
        url = f'{self.base_url}me'
        self.signature = self.calculate_signature(body=body)
        headers = self.get_headers()
        response_data = requests.get(url=url, headers=headers)
        if response_data.status_code == 200:
            return response_data.json()
        else:
            if response_data.status_code in range(400, 600):
                error = response_data
                msg = f'Status: {error.status_code}, details: {error.reason}'
                raise SoSApiException(msg)
