import os
from flask import Blueprint, request, jsonify, make_response, current_app
from flask.views import MethodView
import hashlib, binascii, uuid
import jwt
import datetime
from .. import db

bp = Blueprint('api', __name__, url_prefix='/')


class TestAPI(MethodView):

    def get(self):
        return make_response(jsonify({'Mensaje': 'Funciona bien!'}))

class RegisterUserAPI(MethodView):

    def post(self):
        data = request.get_json()
        if data is None:
            return make_response(jsonify({'message':'Specify the name and passwd'}))
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
        if data is None:
            return make_response(jsonify({'message':'Specify the name and passwd'}))
        if 'name' in data and 'passwd' in data:
            name = data["name"]
            passwd = data["passwd"]

            cur = db.connection.cursor()
            cur.execute('select * from User where NAME="'+name+'"')
            rv = cur.fetchall()
            if not rv:
                return make_response(jsonify({'message':'Specify a valid name and passwd'}))
            stored_passwd = rv[0][2]

            salt = stored_passwd[64:]
            hased_passwd = hashlib.sha256(passwd.encode() + salt.encode()).hexdigest()

            if hased_passwd == stored_passwd[:64]:
                token = jwt.encode({'user': name, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)}, current_app.config['SECRET_KEY'])
                print(token)
                return jsonify({'token': token.decode('UTF-8')})
            else:
                return jsonify('Could not verify!', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})

        return make_response(jsonify({'message':'Specify the name and passwd'}))

    def get(self):
        return make_response(jsonify({'response':'Todo correcto!'})) 

class CheckJWT(MethodView):

    def post(self):
        data = request.get_json()
        if data is None:
            return make_response(jsonify({'message':'No JSON content found on the request'}))
        if 'token' in data:
            recived_token = data['token']

            try:
                data = jwt.decode(recived_token, current_app.config['SECRET_KEY'])
            except jwt.ExpiredSignatureError:
                return make_response(jsonify({'message':'Token expired'}))
            except :
                return make_response(jsonify({'message':'Token invalid'}))

            return make_response(jsonify({'message':'Va bien la cosa'}))

        return make_response(jsonify({'message':'No field named token found'}))


register_user_api = RegisterUserAPI.as_view('register')
login_user_api  = LoginUserApi.as_view('login')
check_jwt_api = CheckJWT.as_view('check')
test_api = TestAPI.as_view('test')
bp.add_url_rule('/login', view_func=login_user_api, methods=['POST', 'GET'])
bp.add_url_rule('/register', view_func=register_user_api, methods=['POST', 'GET'])
bp.add_url_rule('/check', view_func=check_jwt_api, methods=['POST'])
bp.add_url_rule('/', view_func=test_api, methods=['POST', 'GET'])
