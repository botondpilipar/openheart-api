from fastapi import FastAPI
from src.api.configuration import MainConfiguration, RuntimeConfiguration
import pydantic

app: FastAPI = MainConfiguration.RUNTIME.app

@app.get('/query/')
async def read_parameters(kernel_version: str, module_name: str | None):
    return {}

@app.get('/versions/')
async def read_kernel_versions():
    return {}
