from fastapi import FastAPI, Depends
from ctxdb.server.core import ContextDB, InMemoryDatabase
from ctxdb.server.api.routes import setup_routes  # Assuming routes are defined in a 'routes.py' file
from config import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD  # Importing settings

def create_api() -> FastAPI:
    api = FastAPI()
    setup_routes(api, get_ctxdb)
    return api

def get_ctxdb() -> ContextDB:
    return ContextDB(InMemoryDatabase())
        # redis_host=REDIS_HOST,
        # redis_port=REDIS_PORT,
        # redis_password=REDIS_PASSWORD
    

api = create_api()