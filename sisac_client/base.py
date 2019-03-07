from bs4 import BeautifulSoup
import base64
import requests

from .settings import SisacSettings
from .parser import SisacParser
from .exceptions import AuthenticationErrorException

class SisacApiClient:
    def __init__(self):
        self.http = requests

    def __get_cookies(self, session_id):
        return {
            SisacSettings.SISAC_COOKIE_ID: session_id
        }

    def __get_payload(self, student_id, password, captcha, comand="CmdLoginSisac"):
        payload = {
            'login'   : student_id,
            'senha'   : password,
            'conta'   : "aluno",
            'captcha' : captcha,
            'comando' : comand
        }

        return payload

    def __to_base64(self, captcha):
        return "data:image/png;base64,{0}".format(str(base64.b64encode(captcha).decode("utf-8")))

    """
    Returns a valid session id and a valid captcha image in base64 format
    """
    def get_login_credentials(self):
        login_page = self.http.get(
            SisacSettings.SISAC_LOGIN_URL,
            timeout=SisacSettings.TIMEOUT
        )
        
        catpcha = self.http.get(
                    SisacSettings.SISAC_CAPTCHA_URL,
                    stream=True,
                    cookies=self.__get_cookies(login_page.cookies[SisacSettings.SISAC_COOKIE_ID]),
                    timeout=SisacSettings.TIMEOUT)

        return {
            "session_id": login_page.cookies[SisacSettings.SISAC_COOKIE_ID],
            "captcha_image_base64": self.__to_base64(catpcha.content)
        }

    def login(self, session_id, student_id, password, captcha):
        payload = self.__get_payload(student_id, password, captcha)
        
        response = self.http.post(
            SisacSettings.SISAC_LOGIN_FORM_URL,
            data=payload,
            cookies=self.__get_cookies(session_id),
            timeout=SisacSettings.TIMEOUT)

        if response.url != SisacSettings.SISAC_HOME_URL:
            raise AuthenticationErrorException()
        else:
            return {
                'session_id': session_id
            }

    def logout(self, session_id):
        response = self.http.get(
            SisacSettings.SISAC_LOGOUT_URL,
            cookies=self.__get_cookies(session_id),
            timeout=SisacSettings.TIMEOUT
        )

    def atividades_complementares(self, session_id):
        response = self.http.get(
            SisacSettings.SISAC_HOME_URL,
            cookies=self.__get_cookies(session_id),
            timeout=SisacSettings.TIMEOUT
        )

        if response.url != SisacSettings.SISAC_HOME_URL or "Tipo de conta" in str(response.text):
            raise AuthenticationErrorException()
        else:
            sisac_parser = SisacParser(response.text)
            return {
                "student_name": sisac_parser.student_name,
                "total_hours" : sisac_parser.total_hours,
                "categories"  : sisac_parser.categories
            }