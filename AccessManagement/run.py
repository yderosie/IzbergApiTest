from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

import user
import routes

app = Flask(__name__)
api = Api(app)

app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
jwt = JWTManager(app)

api.add_resource(routes.UserLogin, '/api/login/')
api.add_resource(routes.AddPokeType, '/api/group/<type>/add/')
api.add_resource(routes.RemovePokeType, '/api/group/<type>/remove/')
api.add_resource(routes.GetUserInfo, '/api/user/me/')

if __name__ == "__main__":
    app.run(debug=True)
