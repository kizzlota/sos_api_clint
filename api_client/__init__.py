__version__ = '1.0'
__author__ = "sos data team"

import logging
import time
from sys import stdout

from .api_exceptions import SoSApiException
from .authentication import AuthenticationApi
from .upload_pros import UploadProProfileApi
from .general_api import GeneralApiEndpoints


class Sospy:
    '''
    Star Of Service python client
    '''

    def __init__(self, url, token=None, secret=None, username=None, password=None, authorization_key=None,
                 logger_level=20, user_agent=None):
        self.url = url
        self.username = username
        self.password = password
        self.authorization_key = authorization_key
        self.user_agent = user_agent
        self.logger_level = logger_level
        self.logger = self.get_logger()
        self.token = token
        self.secret = secret
        self.validate_setup()
        self.authentication = self.authenticate()
        self.general_api = self.get_general_api()
        self.pro_uploader = self.get_pro_uploader()

    def validate_setup(self):
        if not self.url:
            raise SoSApiException('Incorrect url')
        if 'starofservice.com' not in self.url:
            raise SoSApiException('Incorrect url')
        if not self.username and not self.username and not self.authorization_key:
            raise SoSApiException('Incorrect credentials')

    def get_logger(self):
        logger = logging.getLogger('sos api client')

        format_string = '%(asctime)s - %(levelname)s - [{app_name}] - %(filename)s - line: %(lineno)d - %(message)s'
        formatter = logging.Formatter(format_string)
        logging.Formatter.converter = time.gmtime

        stream_handler = logging.StreamHandler(stream=stdout)
        stream_handler.setFormatter(formatter)

        logger.setLevel(level=self.logger_level)
        logger.addHandler(stream_handler)

        return logger

    def authenticate(self):
        if not self.token and not self.secret:
            client = AuthenticationApi(
                base_url=self.url,
                username=self.username,
                password=self.password,
                key=self.authorization_key,
                user_agent=self.user_agent
            )

            if self.username and self.password:
                response = client.login()
                self.token = response.get('token')
                self.secret = response.get('secret')
                return client
            elif self.authorization_key:
                response = client.login_key(key=self.authorization_key)
                self.token = response.get('token')
                self.secret = response.get('secret')
                return client
            else:
                raise SoSApiException('Unauthorised')

    def get_general_api(self):
        if self.token and self.secret:
            general_api = GeneralApiEndpoints(
                token=self.token,
                secret=self.secret,
                base_url=self.url,
                user_agent=self.user_agent
            )
            return general_api
        else:
            raise SoSApiException('Unauthorised')

    def get_pro_uploader(self):
        if self.token and self.secret:
            upload_api = UploadProProfileApi(
                token=self.token,
                secret=self.secret,
                base_url=self.url,
                logger=self.logger,
                user_agent=self.user_agent
            )
            return upload_api
