"Module for runtime and static configurations of openheart-api API backend"

from os import getenv
from pathlib import Path
from fastapi import FastAPI
from mysql.connector import connect


class DatabaseConfigration:
    DATABASE_HOST = getenv('DATABASE_HOST')
    DATABASE_PORT = getenv('DATABASE_PORT')
    DATABASE_USER = getenv('DATABASE_USER')
    DATABASE_PASSWORD_FILE = getenv('DATABASE_PASSWORD_FILE')
    DATABASE_PASSWORD = Path(DATABASE_PASSWORD_FILE).read_text(encoding='UTF-8').strip()
    DATABASE_NAME = "kernels"

    @property
    def host(self):
        return DatabaseConfigration.DATABASE_HOST

    @property
    def port(self):
        return DatabaseConfigration.DATABASE_PORT

    @property
    def user(self):
        return DatabaseConfigration.DATABASE_USER

    @property
    def password_file(self):
        return DatabaseConfigration.DATABASE_PASSWORD_FILE

    @property
    def password(self):
        return DatabaseConfigration.DATABASE_PASSWORD

    @property
    def database_name(self):
        return DatabaseConfigration.DATABASE_NAME

    @staticmethod
    def create_db_if_does_not_exist(connection_obj, name):
        cursor = connection_obj.cursor()
        cursor.execute('SHOW DATABASES')
        databases = list(cursor)

        if name not in databases:
            cursor.execute(f'CREATE DATABASE {name}')

    def connect(self):
        mysql_connection = connect(user=self.user, password=self.password, host=self.host)
        self.create_db_if_does_not_exist(mysql_connection, self.database_name)


class MainConfiguration:
    APP_NAME = getenv('APP_NAME')
    FAST_API_PORT = getenv('FAST_API_PORT')
    RUNTIME = None

    def __init__(self, app: FastAPI):
        if MainConfiguration.RUNTIME is None:
            MainConfiguration.RUNTIME = RuntimeConfiguration(app, DatabaseConfigration())

    @property
    def app_name(self):
        return MainConfiguration.APP_NAME

    @property
    def fast_api_port(self):
        return MainConfiguration.FAST_API_PORT


class RuntimeConfiguration:
    def __init__(self, app: FastAPI, database: DatabaseConfigration) -> None:
        self.__app = app
        self.__database = database

    @property
    def app(self):
        return self.__app

    @property
    def database(self):
        return self.__database
