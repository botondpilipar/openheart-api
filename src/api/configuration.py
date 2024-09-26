from os import getenv
from pathlib import Path
from fastapi import FastAPI


class MainConfiguration:
    APP_NAME = getenv('APP_NAME')
    FAST_API_PORT = getenv('FAST_API_PORT')
    DATABASE_HOST = getenv('DATABASE_HOST')
    DATABASE_PORT = getenv('DATABASE_PORT')
    DATABASE_USER = getenv('DATABASE_USER')
    DATABASE_PASSWORD_FILE = getenv('DATABASE_PASSWORD_FILE')
    DATABASE_PASSWORD = Path(DATABASE_PASSWORD_FILE).read_text(encoding='UTF-8').strip()
    RUNTIME = None
    
    def __init__(self, app: FastAPI):
        if MainConfiguration.RUNTIME is None:
            MainConfiguration.RUNTIME = RuntimeConfiguration(app)
    
class RuntimeConfiguration:
    def __init__(self, app: FastAPI) -> None:
        self.__app = app
        
    @property
    def app(self):
        return self.__app