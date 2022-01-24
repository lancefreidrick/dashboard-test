# pylint: disable=global-statement

from datetime import datetime
import psycopg2
from server.config.logger import log
from server.config.environment import config

__connection_pg = None

def start(connection_string: str):
    global __connection_pg
    cursor = None
    try:
        addr = connection_string.split('@')[1]
        log.info(f'pgdb:    Connecting to the Postgresql database ({addr})...', )
        __connection_pg = psycopg2.connect(connection_string)
        cursor = __connection_pg.cursor()
        cursor.execute('SELECT VERSION()')
        log.info(f'pgdb:    Connected to {cursor.fetchone()}')

    except psycopg2.DatabaseError as error:
        log.error('pgdb:    ERROR on database connection')
        log.error(f'pgdb:    {str(error)}')
    finally:
        if cursor:
            cursor.close()

def func(func_name, *params):
    global __connection_pg
    fn = 'db.func'
    log.debug(f'{fn}: {func_name} {str(*params)}')
    try:
        start_time = datetime.now()
        mapped_data = []

        with __connection_pg.cursor() as cursor:
            cursor.callproc(func_name, *params)
            data = cursor.fetchall()

            column_names = [d[0] for d in cursor.description]
            mapped_data = [dict(zip(column_names, list(values))) for values in data]

            __connection_pg.commit()
            cursor.close()

        end_time = datetime.now()
        execution_time = end_time - start_time
        log.debug(f'{fn}: {func_name} - {execution_time.total_seconds()}s')
        return mapped_data
    except (psycopg2.InterfaceError, psycopg2.OperationalError) as error:
        log.error(f'{fn}: Database server connection error, restarting connection.')
        start(config.pg_connection_string)
        log.info(f'{fn}: Server reconnected, retrying query..')
    except (psycopg2.ProgrammingError, psycopg2.DatabaseError) as error:
        __connection_pg.rollback()
        log.error(f'{fn}: Internal server error, rolling back..')
        raise error

def execute_query(query, *param):
    """
    This is only used for test helper. Do not use it for production queries.
    """
    global __connection_pg
    try:
        with __connection_pg.cursor() as cursor:
            cursor.execute(query, *param)
            __connection_pg.commit()
            cursor.close()
            return True
    except (psycopg2.ProgrammingError,
            psycopg2.DatabaseError) as error:
        __connection_pg.rollback()
        log.warning('Internal server error, rolling back...')
        raise error
