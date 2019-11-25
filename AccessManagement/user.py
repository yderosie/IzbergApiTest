from tinydb import TinyDB, Query
from passlib.hash import pbkdf2_sha256 as sha256

db = TinyDB('../db.json')

class UserModel():
    table = db.table('users')

    @classmethod
    def find_by_username(self, username):
        return self.table.get(Query()['username'] == username)

    @classmethod
    def return_user_infos(self, userid):
        user = self.table.get(doc_id = userid)
        ret = {
            'firstname': user['firstname'],
            'lastname': user['lastname'],
            'username': user['username'],
            'poketypes': user['poketypes']
        }
        return ret

    @classmethod
    def add_poke_type_in_user(self, userid, poketype):
        user = self.table.get(doc_id = userid)
        if not poketype in user["poketypes"]:
            user["poketypes"].append("flying")
            return self.table.write_back([user])
        return None


    @classmethod
    def remove_poke_type_in_user(self, userid, poketype):
        user = self.table.get(doc_id = userid)
        if poketype in user["poketypes"]:
            user["poketypes"].remove("flying")
            return self.table.write_back([user])
        return None

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password + "123")

    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password + "123", hash)
