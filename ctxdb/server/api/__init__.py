import os
from fastapi import FastAPI, HTTPException
from ctxdb.server.core import ContextDB
from ctxdb.common.models import BaseContext, Context
from ctxdb.common.utils import encode
REDIS_HOST = os.environ["REDIS_HOST"]
REDIS_PORT = os.environ["REDIS_PORT"]
REDIS_PASSWORD = os.environ["REDIS_PASSWORD"]
app = FastAPI()
ctxdb = ContextDB()


@app.post("/ctxdb/contexts", response_model=BaseContext)
def add_context(context: BaseContext):
    try:
        context: Context = Context(input=context.input, output=context.output, context=encode(context.input))
        new_id = ctxdb.add_context(context)
        return {
            "id": new_id,
            **context.dict()
        }  # Assuming add_context returns a new id
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/ctxdb/contexts/{idx}", response_model=BaseContext)
def get_context(idx: str):
    context = ctxdb.get_context(idx)
    if context:
        return context
    else:
        raise HTTPException(status_code=404, detail="Context not found")


@app.delete("/ctxdb/contexts/{idx}")
def delete_context(idx: str):
    if ctxdb.delete_context(idx):
        return {"message": "Context deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Context not found")


@app.put("/ctxdb/contexts/{idx}", response_model=BaseContext)
def update_context(idx: str, context: BaseContext):
    try:
        updated_context = ctxdb.update_context(idx, context.dict())
        if updated_context:
            return updated_context
        else:
            raise HTTPException(status_code=404, detail="Context not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/ctxdb/contexts/query", response_model=list[BaseContext])
def query_context(query: str):
    try:
        contexts = ctxdb.query(query)
        return contexts
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
