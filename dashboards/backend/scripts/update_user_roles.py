""" update_user_roles.py """
from sys import stderr
import json
from bson import ObjectId
from pymongo import MongoClient

ADMIN = (10, 'Admin')
STAFF = (20, 'Staff')
MERCHANT_ADMIN = (30, 'Merchant Admin')
MERCHANT_STAFF = (40, 'Merchant Staff')
MERCHANT_AGENT = (50, 'Merchant Agent')

class Person:
    def __init__(self, data):
        self.id = data.get('_id')
        self.first_name = data.get('firstname')
        self.last_name = data.get('lastname')
        self.email = data.get('email')
        self.hashed_password = data.get('password')
        self.is_admin = data.get('is_admin') or False
        self.scopes = data.get('scopes')
        self.permissions = data.get('permissions')

    def __str__(self):
        return '{},{},{},{}'.format(self.id, self.first_name, self.last_name, self.email)

    def json(self) -> dict:
        data = dict()
        data['firstname'] = self.first_name or self.email.split('@')[0]
        data['lastname'] = self.last_name or 'Qwikwire'
        data['email'] = self.email
        data['scopes'] = self.scopes or {}
        if self.hashed_password:
            data['password'] = self.hashed_password

        if self.is_admin:
            data['role'] = {'id': ADMIN[0], 'name': ADMIN[1]}
        elif self.scopes and len(self.scopes) >= 1:
            data['role'] = {'id': MERCHANT_ADMIN[0], 'name': MERCHANT_ADMIN[1]}
        else:
            data['role'] = {'id': STAFF[0], 'name': STAFF[1]}

        data['isEnabled'] = True
        data['isAccountConfirmed'] = bool(self.hashed_password)

        return data

def open_config():
    try:
        config_data = open('.env', 'r')
        return json.loads(config_data.read())
    except IOError as e:
        print(e, file=stderr)
        return {}

def start():
    config = open_config()
    client = MongoClient(host=config['mongohost'], port=config['mongoport'])
    users_db = client['directory']['users']
    users = users_db.find()

    for user in users:
        person = Person(user)
        result = users_db.update_one({'_id': ObjectId(person.id)}, {
            '$set': person.json(),
            '$unset': {
                'is_admin': True,
                'permissions': True,
                'slug': True
            }
        })
        print(person, result.modified_count)

def populate_old_data():
    # Backup all the users into the users.json just in case something goes wrong
    with open('./scripts/users.json') as directory:
        directory_data = json.load(directory)
        users = directory_data.get('users')
        config = open_config()
        client = MongoClient(host=config['mongohost'], port=config['mongoport'])
        client['directory']['users'].delete_many({'email': {'$exists': True}})
        client['directory']['users'].insert_many(users)

# populate_old_data()
start()
