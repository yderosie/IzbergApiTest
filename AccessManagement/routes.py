
from flask_restful import Resource, reqparse
from flask_jwt_extended import (create_access_token, jwt_required, get_jwt_identity, get_raw_jwt)
from urllib.request import Request, urlopen
import urllib.error
import datetime

from user import UserModel

parser = reqparse.RequestParser()
parser.add_argument('username', help = 'This field cannot be blank', required = True)
parser.add_argument('password', help = 'This field cannot be blank', required = True)

class UserLogin(Resource):
    def post(self):
        data = parser.parse_args()
        current_user = UserModel.find_by_username(data['username'])

        if not current_user:
            return {'message': 'User {} doesn\'t exist'.format(data['username'])}

        if UserModel.verify_hash(data['password'], current_user['password']):
            access_token = create_access_token(identity = current_user.doc_id, expires_delta = datetime.timedelta(hours=1))
            return {
                'message': 'Logged in as {}'.format(current_user["username"]),
                'access_token': access_token,
                }
        else:
            return {'message': 'Wrong credentials'}


class AddPokeType(Resource):
    @jwt_required
    def post(self, type):
        current_userId = get_jwt_identity()
        req = Request('https://pokeapi.co/api/v2/type/' + type + '/', headers={'User-Agent': 'Mozilla/5.0'})
        try :
            resp = urlopen(req)
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return {
                    'error': "Le type voulant être ajouté n'existe pas"
                }
        if (UserModel.add_poke_type_in_user(current_userId, type) != None):
            return {'status': "successful", "message": "Le type a bien été ajouté"}
        return {
            'status': "error",
            "message": "Le type voulant être ajouté est déja present"
        }

class RemovePokeType(Resource):
    @jwt_required
    def post(self, type):
        current_userId = get_jwt_identity()
        if (UserModel.remove_poke_type_in_user(current_userId, type) != None):
            return {'status': "successful", "message": "Le type a bien été supprimé"}
        return {
            'status': "error",
            "message": "Le type voulant être supprimé n'est pas présent"
        }

class GetUserInfo(Resource):
    @jwt_required
    def get(self):
        current_userId = get_jwt_identity()
        data = UserModel.return_user_infos(current_userId)
        return {'status': "successful", 'data': data}
