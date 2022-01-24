""" populate.py """
from server.config import database

def populate_directory_tables():
    with open('./tests/data/directory.sql') as file:
        database.execute_query(file.read())

def populate_invoicing_tables():
    with open('./tests/data/invoicing.sql') as file:
        database.execute_query(file.read())
    
def populate_auditing_tables():
    with open('./tests/data/auditing.sql') as file:
        database.execute_query(file.read())

def remove_tables_data():
    with open('./tests/data/cleanup.sql') as file:
        database.execute_query(file.read())
