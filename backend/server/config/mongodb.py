# pylint: disable=global-statement
from pymongo import MongoClient, monitoring
from server.config.logger import log

__connection = None

class ServerLogger(monitoring.ServerListener):
    def opened(self, event):
        log.info('mongodb: Connection has been opened %s', event.server_address)

    def closed(self, event):
        pass

    def description_changed(self, event):
        pass

def start(host: str, port: int):
    global __connection
    log.info('mongodb: Connecting to the server...')

    monitoring.register(ServerLogger())
    __connection = MongoClient(host, port)

def stop():
    global __connection
    __connection.close()

def get(dbname=None):
    if dbname is None:
        return __connection
    return __connection[dbname]
