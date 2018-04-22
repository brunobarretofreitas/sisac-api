from bs4 import BeautifulSoup
import base64
import requests as http_request

from rest_framework.validators import ValidationError
from .settings import SisacApiSettings, AuthenticationErrorException
from .parser import SisacParser

class SisacApiClient:
    def __init__(self):
        self.settings = SisacApiSettings()

    def get_payload(self, student_id, password, captcha, comand="CmdLoginSisac"):
        payload = {
            'login'   : student_id,
            'senha'   : password,
            'conta'   : "aluno",
            'captcha' : captcha,
            'comando' : comand
        }

        return payload

    """
    Returns the Captcha Image in base64 format
    """
    def get_captcha_image(self, cookies):
        captcha_request = http_request.get(self.settings.SISAC_CAPTCHA_URL, stream=True, verify=False, cookies=cookies)
        captcha_base64_format = "data:image/png;base64," + str(base64.b64encode(captcha_request.content).decode("utf-8"))
        return captcha_base64_format

    """
    Returns a valid session id and a valid captcha image in base64 format
    """
    def login_page(self):
        sisac_request = http_request.get(self.settings.SISAC_LOGIN_URL)
        response = {
            "session_id": sisac_request.cookies[self.settings.SISAC_COOKIE_ID],
            "captcha_image": self.get_captcha_image(dict(JSESSIONID=sisac_request.cookies[self.settings.SISAC_COOKIE_ID]))
        }
        return response

    def login(self, session_id, student_id, password, captcha):
        sisac_request = http_request.post(
            self.settings.SISAC_LOGIN_FORM_URL,
            verify=False,
            cookies=dict(JSESSIONID=session_id),
            data=self.get_payload(student_id, password, captcha))

        if sisac_request.url != self.settings.SISAC_HOME_URL:
            raise AuthenticationErrorException()
        else:
            return session_id
    
    def home_page(self, session_id):
        cookies = dict(JSESSIONID=session_id)
        sisac_request = http_request.get(self.settings.SISAC_HOME_URL, verify=False, cookies=cookies)
        if sisac_request.url != self.settings.SISAC_HOME_URL or "Tipo de conta" in str(sisac_request.content):
            raise AuthenticationErrorException()
        else:
            sisac_parser = SisacParser(sisac_request.content)
            return {
                "student_name" : sisac_parser.student_name,
                "total-hours"  : sisac_parser.total_hours,
                "categories"   : sisac_parser.categories
            }