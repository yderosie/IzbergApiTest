from tinydb import TinyDB, Query
from passlib.hash import pbkdf2_sha256

db = TinyDB('db.json')

table = db.table('users')

secret = "123"

hash = pbkdf2_sha256.hash("test" + secret)

table.insert({'firstname': "user1", "lastname": "test", "username": "test1", "password": hash, "poketypes": []})
table.insert({'firstname': "user2", "lastname": "test", "username": "test2", "password": hash, "poketypes": []})
