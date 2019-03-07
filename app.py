from flask import Flask, Response, jsonify, request
import requests
import json
import os
from dotenv import load_dotenv

from sisac_client import SisacApiClient, SisacSettings, AuthenticationErrorException

app = Flask(__name__)
sisac_api_client = SisacApiClient()
load_dotenv()

# Função para retornar mensagem padrão de timeout
def timeout_error():
    return {
        'message': SisacSettings.TIMEOUT_ERROR
    }, 408

# Função para validar a API_KEY
def valid_api_key(request_data):
    if not request_data.get('api_key', None):
        return False
    elif request_data.get('api_key', None) != os.getenv('API_KEY'):
        return False
    return True


# Rota para obter o id da sessão a ser utilizada, juntamente com o captcha em formato base64
@app.route("/login-credentials", methods=['GET'])
def login_credentials():
    # Validando o API_KEY
    if not valid_api_key(request.args):
        return jsonify({
            'message': 'É necessário informar uma api_key válida'
        }), 400

    try:
        data = sisac_api_client.get_login_credentials()
        return jsonify(data), 200
    except requests.exceptions.ConnectTimeout:
        data = {
            'message': SisacSettings.TIMEOUT_ERROR
        }

        return jsonify(data), 408

# Rota para realizar login na aplicação
@app.route("/login", methods=['POST'])
def login():
    # Validando o API_KEY
    if not valid_api_key(request.args):
        return jsonify({
            'message': 'É necessário informar uma api_key válida'
        }), 400
    
    try:
        request_data = json.loads(request.data)
        
        data = sisac_api_client.login(
            request_data['session_id'],
            request_data['matricula'],
            request_data['senha'],
            request_data['captcha']
        )

        return jsonify({
            'message': 'Login realizado com sucesso',
            **data
        }), 200
    except requests.exceptions.ConnectTimeout:
        data, status_code = timeout_error()
    except AuthenticationErrorException:
        status_code = 400
        data = {
            'message': SisacSettings.AUTH_ERROR 
        }
    except KeyError:
        status_code = 400
        data = {
            'message': "Os parâmetros (session_id, matricula, senha, captcha) devem ser fornecidos"
        }

    return jsonify(data), status_code

# Rota para deslogar da aplicação
@app.route("/logout", methods=['POST'])
def logout():
    # Validando o API_KEY
    if not valid_api_key(request.args):
        return jsonify({
            'message': 'É necessário informar uma api_key válida'
        }), 400

    try:
        request_data = json.loads(request.data)
        sisac_api_client.logout(request_data['session_id'])
        status_code = 200
        data = {
            'message': 'Logout realizado com sucesso'
        }
    except requests.exceptions.ConnectTimeout:
        data, status_code = timeout_error()
    except KeyError:
        status_code = 400
        data = {
            'message': 'Os parâmetros (session_id) devem ser fornecidos'
        }

    return jsonify(data), status_code

# Rota para obter todas as atividades complementares do aluno
@app.route("/atividades-complementares", methods=['GET'])
def atividades_complementares():
    # Validando o API_KEY
    if not valid_api_key(request.args):
        return jsonify({
            'message': 'É necessário informar uma api_key válida'
        }), 400

    try:
        status_code = 200
        data = sisac_api_client.atividades_complementares(request.args.get('session_id'))
    except requests.exceptions.ConnectTimeout:
        data, status_code = timeout_error()
    except AuthenticationErrorException:
        status_code = 400
        data = {
            'message': SisacSettings.AUTH_ERROR
        }
    
    return jsonify(data), status_code


if __name__ == '__main__':
    if os.getenv("API_KEY"):
        app.run()
    else:
        raise Exception('.env API_KEY not found')