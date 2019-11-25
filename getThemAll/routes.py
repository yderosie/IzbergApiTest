from flask import request
from flask_restful import Resource, reqparse

from pokemon import Pokemon

class GetAllPokemonAccess(Resource):
    def get(self):
        if not 'Authorization' in request.headers:
            return {"msg": "Missing Authorization Header"}, 401
        project_secret_key = request.headers.get('Authorization')
        types = Pokemon.getPokeTypeUserAccess(project_secret_key)
        if not 'types' in types:
            return types['error']
        pokemon = Pokemon.getPokemonListForPokeTypeUserAccess(types['types'])
        if not 'pokemon' in pokemon:
            return {'erreur': pokemon['erreur']}
        return {'pokemon': pokemon['pokemon']}

class GetPokemonDetailByIdOrName(Resource):
    def get(self, pokemon):
        pokemonDetail = Pokemon.getPokemonByIdOrName(pokemon)
        if not 'pokemon' in pokemonDetail:
            return {'error': pokemonDetail['error']}
        if not 'Authorization' in request.headers:
            return {"msg": "Missing Authorization Header"}, 401
        project_secret_key = request.headers.get('Authorization')
        types = Pokemon.getPokeTypeUserAccess(project_secret_key)
        if not 'types' in types:
            return types['error']
        for type in pokemonDetail['pokemon']['types']:
            if type['type']['name'] in types['types']:
                return {'pokemonDetail': pokemonDetail}
        return {'error': 'Vous devez ajouté le type du pokemon avant de voir plus d\'informations'}
