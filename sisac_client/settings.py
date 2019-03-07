class SisacSettings:
    SISAC_LOGIN_URL = "https://sistemas.quixada.ufc.br/sisac/"
    SISAC_HOME_URL  = "https://sistemas.quixada.ufc.br/sisac/aluno_listar_atividades_complementares.jsp";
    SISAC_COOKIE_ID = "JSESSIONID"
    SISAC_CAPTCHA_URL = "https://sistemas.quixada.ufc.br/sisac/captcha.jpg"
    SISAC_LOGIN_FORM_URL = "https://sistemas.quixada.ufc.br/ServletCentral"
    SISAC_LOGOUT_URL = "https://sistemas.quixada.ufc.br/ServletCentral?comando=CmdLogoutSisac"
    TIMEOUT = 10

    TIMEOUT_ERROR = 'Não foi possível estabeler uma conexão com o sistema SISAC'
    AUTH_ERROR    = 'Não foi acessar o sistema com as credenciais fornecidas'
    SERVER_UNAVAILABLE = 'O servidor da aplicação não está disponível'
