""" update_user_enabled_flag.py """
import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

host = os.environ.get('MONGODB_HOST')
port = int(os.environ.get('MONGODB_PORT', 27017))

db_connection = MongoClient(host, port)
directory_db = db_connection.get_database(name='directory')
users_collection = directory_db.get_collection('users')

def updateEnabledFlagOnAllUsers():
    update_result = users_collection.update_many({
        'email': {'$exists': True}
    }, {
        '$set': {
            'isEnabled': True,
            'isAccountConfirmed': False
        }
    })
    print('Matched: {} Modified {}'.format(
        update_result.matched_count,
        update_result.modified_count
    ))

def updateAccountConfirmationFlagForUsersWithPasswords():
    update_result = users_collection.update_many({
        'password': {'$exists': True}
    }, {
        '$set': {
            'isAccountConfirmed': True
        }
    })
    print('Matched: {} Modified {}'.format(
        update_result.matched_count,
        update_result.modified_count
    ))

updateEnabledFlagOnAllUsers()
updateAccountConfirmationFlagForUsersWithPasswords()
