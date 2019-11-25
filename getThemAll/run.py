from flask import Flask
from flask_restful import Api

import routes

app = Flask(__name__)
api = Api(app)

api.add_resource(routes.GetAllPokemonAccess, '/api/pokemon/')
api.add_resource(routes.GetPokemonDetailByIdOrName, '/api/pokemon/<pokemon>/')

if __name__ == "__main__":
    app.run(debug=True, port=5001)
