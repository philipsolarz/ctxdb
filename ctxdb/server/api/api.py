from fastapi import FastAPI, Depends
from ctxdb.server.core import ContextDB, InMemoryDatabase
from ctxdb.server.api.routes import setup_routes  # Assuming routes are defined in a 'routes.py' file
from config import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD  # Importing settings

def create_api(ctxdb: ContextDB) -> FastAPI:
    api = FastAPI()
    setup_routes(api, ctxdb)
    return api

def create_ctxdb() -> ContextDB:
    ctxdb = ContextDB(InMemoryDatabase())
    return ctxdb
        # redis_host=REDIS_HOST,
        # redis_port=REDIS_PORT,
        # redis_password=REDIS_PASSWORD
    


ctxdb = create_ctxdb()
api = create_api(ctxdb)