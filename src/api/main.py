"""Module for running FastAPI as main application"""
from fastapi import FastAPI
# pylint: disable=unused-import
import src.api.query_routes
# pylint: disable=unused-import
from src.api.configuration import MainConfiguration

app = FastAPI(debug=True, title=MainConfiguration.APP_NAME)
config = MainConfiguration(app)


def main():
    pass


if __name__ == '__main__':
    main()
