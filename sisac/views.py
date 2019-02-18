from rest_framework import views
from rest_framework.response import Response
from rest_framework.validators import(
    ValidationError,
)
from rest_framework.exceptions import (
    AuthenticationFailed,
    NotAuthenticated
)
from .sisac_client import (
    SisacApiClient,
    SisacApiSettings,
    AuthenticationErrorException,
)

from django.views.decorators.csrf import csrf_exempt

from .settings import API_SECRET_KEY

def validate_request(**kwargs):
    error_message = []
    for key, val in kwargs.items():
        if not val:
            error_message.append({key: "Este campo é obrigatório"})
        if len(error_message):
            raise ValidationError({"error": error_message})

    if kwargs.get('token', None) != API_SECRET_KEY:
        raise ValidationError({"token": "Token Inválido"})


@csrf_exempt
class LoginPageView(views.APIView):

    def __init__(self):
        self.sisac_client = SisacApiClient()
        self.sisac_settings = SisacApiSettings()
        

    def get(self, request, format=None):
        token = request.query_params.get('token', None)

        validate_request(token=token)
        login_page_attributes = self.sisac_client.login_page()
        return Response(login_page_attributes)

    def post(self, request, format=None):
        session_id = request.data.get('session_id')
        student_id = request.data.get('login')
        password = request.data.get('senha')
        captcha = request.data.get('captcha')
        token = request.data.get('token', None)

        validate_request(session_id=session_id, student_id=student_id, password=password, captcha=captcha, token=token)

        try:
            self.sisac_client.login(session_id, student_id, password, captcha)
            return Response(status=200,data={"message": "Login realizado com sucesso", "session_id": session_id})
        except AuthenticationErrorException:
            raise AuthenticationFailed({"authentication_error": "Erro ao realizar autenticação"})

class HomePageView(views.APIView):
    
    def __init__(self):
        self.sisac_client = SisacApiClient()
        self.sisac_settings = SisacApiSettings()
    
    def get(self, request, format=None):
        session_id = request.query_params.get('session_id', None)
        token = request.query_params.get('token', None)

        validate_request(token=token, session_id=session_id)

        session_id = request.query_params.get('session_id')
        if not session_id:
            raise ValidationError({"session_id": "É necessário informar o id da sessão"})
        
        try:
            sisac_data = self.sisac_client.home_page(session_id)
            return Response(sisac_data)
        except AuthenticationErrorException:
            raise NotAuthenticated({"login_required": "Esta sessão de usuário não está logada"})