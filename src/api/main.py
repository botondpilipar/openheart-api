from os import getenv, path
from fastapi import FastAPI, APIRouter
from pathlib import Path
from mysql import connector

from configuration import MainConfiguration, RuntimeConfiguration

    
app = FastAPI(debug=True, title=MainConfiguration.APP_NAME)
config = MainConfiguration(app)

from query_routes import Queries

def create_db_if_does_not_exist(connection_obj, name):
    cursor = connection_obj.cursor()
    cursor.execute('SHOW DATABASES')
    databases = [res for res in cursor]
    
    if not name in databases:
        cursor.execute(f'CREATE DATABASE {name}')
    
def main():
    mysql_connection = connector.connect(
                            user=config.DATABASE_USER,
                            password=config.DATABASE_PASSWORD,
                            host=config.DATABASE_HOST)
    create_db_if_does_not_exist(mysql_connection, 'kernels')

    queries = Queries()
    

if __name__ == '__main__':
    main()