from urllib.request import Request, urlopen
import urllib.error
import json

class Pokemon():

    @staticmethod
    def getPokeTypeUserAccess(token):
        reqMApi = Request('http://127.0.0.1:5000/api/user/me/', headers={'User-Agent': 'Mozilla/5.0', 'Authorization': token})
        try :
            respMApi = urlopen(reqMApi)
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return {
                    'error': "Le type voulant être ajouté n'existe pas"
                }
            elif e.code == 401:
                return {
                    'error': "Le token est incorrect ou a expirer"
                }
        except urllib.error.URLError as e:
            return {
                'error': "Management Api n'est pas disponible"
            }
        else:
            user = respMApi.read()
            user = user.decode('utf-8')
            user = json.loads(user)
        return {'types': user['data']['poketypes']}

    @staticmethod
    def getPokemonListForPokeTypeUserAccess(types):
        pokemonList = []
        tmpListAlreadyAdd = []
        for type in types:
            # print("cicicic")
            reqPokeAPi = Request('https://pokeapi.co/api/v2/type/' + type + '/', headers={'User-Agent': 'Mozilla/5.0'})
            try:
                respPokeApi = urlopen(reqPokeAPi)
            except urllib.error.HTTPError as e:
                if e.code == 404:
                    return {
                        'error': "PokeApi indisponible"
                    }
            except urllib.error.URLError as e:
                return {
                    'error': "PokeApi indisponible"
                }
            else:
                pokemonByType = respPokeApi.read()
                pokemonByType = pokemonByType.decode('utf-8')
                pokemonByType = json.loads(pokemonByType)
                for pokemon in pokemonByType['pokemon']:
                    if not pokemon['pokemon']['name'] in tmpListAlreadyAdd:
                        pokemonList.append(pokemon['pokemon'])
                        tmpListAlreadyAdd.append(pokemon['pokemon']['name'])
        return {'pokemon': pokemonList}

    @staticmethod
    def getPokemonByIdOrName(pokemon):
        reqPokeAPi = Request('https://pokeapi.co/api/v2/pokemon/' + pokemon + '/', headers={'User-Agent': 'Mozilla/5.0'})
        try:
            respPokeApi = urlopen(reqPokeAPi)
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return {
                    'error': "Pokemon inexistant"
                }
        except urllib.error.URLError as e:
            return {
                'error': "PokeApi indisponible"
            }
        else:
            pokemonDetail = respPokeApi.read()
            pokemonDetail = pokemonDetail.decode('utf-8')
            pokemonDetail = json.loads(pokemonDetail)
            return {'pokemon': pokemonDetail}
        return {
            'error': "Une erreur est survenue"
        }
