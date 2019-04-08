import os
from flask import Blueprint, request, jsonify, make_response
from flask.views import MethodView
#import haslib, binascii
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
            return make_response(jsonify({'message':rv}))

        return make_response(jsonify({'message':'Specify the name and passwd'}))

    def get(self):
        return make_response(jsonify({'response':'Hola mundo!'})) 

register_user_api = RegisterUserAPI.as_view('register')
test_api = TestAPI.as_view('test')
bp.add_url_rule('/register', view_func=register_user_api, methods=['POST', 'GET'])
bp.add_url_rule('/', view_func=test_api, methods=['POST', 'GET'])
