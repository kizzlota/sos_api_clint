import hmac
import hashlib
import json
import requests
from retrying import retry
from .api_exceptions import SoSApiException, SosApiStatusException


def retry_on_status(exception):
    return isinstance(exception, SosApiStatusException)


class UploadProProfileApi:
    def __init__(self, token, secret, base_url, logger, user_agent):
        self.logger = logger
        self.base_url = base_url
        self.token = token
        self.secret = secret
        self.signature = None
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

    @retry(retry_on_exception=retry_on_status, stop_max_attempt_number=6, wait_fixed=60)
    def upload(self, body):
        url = f'{self.base_url}pro_profiles_batch'
        self.signature = self.calculate_signature(body=body)
        headers = self.get_headers()
        response_data = requests.post(url=url, headers=headers, data=body)
        if response_data.status_code in [200, 201]:
            return response_data.json()
        elif response_data.status_code == 400:
            error = response_data
            msg = 'Bad request'
            if hasattr(error, 'text'):
                details = json.loads(error.text)
                detail = details.get('errors')[0]
                msg = f'Status: {error.status_code}, reason: {error.reason}, details: {detail.get("detail")}'
            raise SosApiStatusException(msg)
        else:
            if response_data.status_code in range(401, 600):
                error = response_data
                msg = f'Status: {error.status_code}, details: {error.reason}'
                raise SoSApiException(msg)
