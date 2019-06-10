from flask import Blueprint, request, jsonify
from ..services.user.userService import UserService
from ..lib.exceptions.argumentException import ArgumentException

user_api = Blueprint('user_api',__name__)

@user_api.route('/create',methods=['POST'])
def create_user():
	name = request.form.get('name')
	email = request.form.get('email')
	password = request.form.get('password')

	args = {
		'name': name, 
		'email': email, 
		'password': password
	}

	service = UserService()
	result = {}
	try:
		result = service.create(args)
	except ArgumentException as e:
		result['error'] = e.value

	return jsonify(result)

@user_api.route('/<int:id>',methods=['GET'])
def get_user(id):
	return "this will be a user"
