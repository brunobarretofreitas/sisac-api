class SisacApiSettings:
    SISAC_LOGIN_URL = "https://sistemas.quixada.ufc.br/sisac/"
    SISAC_HOME_URL  = "https://sistemas.quixada.ufc.br/sisac/aluno_listar_atividades_complementares.jsp";
    SISAC_COOKIE_ID = "JSESSIONID"
    SISAC_CAPTCHA_URL = "https://sistemas.quixada.ufc.br/sisac/captcha.jpg"
    SISAC_LOGIN_FORM_URL = "https://sistemas.quixada.ufc.br/ServletCentral"

    _general_error_messages = {
        'connection_error' : 'Não foi possível estabeler uma conexão com o sistema SISAC',
        'authentication_error': 'Não foi possível fazer o login com as credenciais fornecidas'
    }

    def get_authentication_message(self):
        return dict(authentication_error=self._general_error_messages.get('authentication_error'))

class AuthenticationErrorException(Exception):
    pass

