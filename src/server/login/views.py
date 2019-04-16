import os
from flask import Blueprint, request, jsonify, make_response
from flask.views import MethodView
import hashlib, binascii, uuid
from .. import db

bp = Blueprint('api', __name__, url_prefix='/')


class TestAPI(MethodView):

    def get(self):
        return make_response(jsonify({'Mensaje': 'Funciona bien!'}))

class RegisterUserAPI(MethodView):

    def post(self):
        data = request.get_json()
        if 'name' in data and 'passwd' in data:
            name = data['name']
            passwd = data['passwd']

            cur = db.connection.cursor()
            cur.execute('select * from User where NAME="'+name+'"')
            rv = cur.fetchall()
            if rv:
                return make_response(jsonify({'message':'User already exists'}))
            salt = hashlib.sha256( uuid.uuid4().hex.encode() ).hexdigest()
            hased_passwd = hashlib.sha256(passwd.encode() + salt.encode()).hexdigest()
            hased_passwd = hased_passwd + salt


            cur = db.connection.cursor()
            try:
                cur.execute('INSERT INTO User (name, passwd) VALUES (%s,%s)',(name,hased_passwd))
                db.connection.commit()
                return make_response(jsonify({'message':'User registered'}))
            except Exception as e:
                return make_response(jsonify({'message':'Error in database query.'}))

        return make_response(jsonify({'message':'Specify the name and passwd'}))

    def get(self):
        return make_response(jsonify({'response':'Hola mundo!'})) 

class LoginUserApi(MethodView):

    def post(self):
        data = request.get_json()
        if 'name' in data and 'passwd' in data:
            name = data["name"]
            passwd = data["passwd"]

        return make_response(jsonify({'message':'Specify the name and passwd'}))

    def get(self):
        return make_response(jsonify({'response':'Todo correcto!'})) 
        

register_user_api = RegisterUserAPI.as_view('register')
login_user_api  = LoginUserApi.as_view('login')
test_api = TestAPI.as_view('test')
bp.add_url_rule('/login', view_func=login_user_api, methods=['POST', 'GET'])
bp.add_url_rule('/register', view_func=register_user_api, methods=['POST', 'GET'])
bp.add_url_rule('/', view_func=test_api, methods=['POST', 'GET'])
