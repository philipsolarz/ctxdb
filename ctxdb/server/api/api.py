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


@app.post("/ctxdb/contexts", response_model=Context)
def add_context(context: Context):
    try:
        context.context = encode(context.input)
        # context: Context = Context(input=context.input, output=context.output, context=encode(context.input))
        new_id = ctxdb.add_context(context)
        return {
            "id": new_id,
            **context.dict()
        }  # Assuming add_context returns a new id
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/ctxdb/contexts/{idx}", response_model=Context)
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


@app.put("/ctxdb/contexts/{idx}", response_model=Context)
def update_context(idx: str, context: Context):
    try:
        updated_context = ctxdb.update_context(idx, context.dict())
        if updated_context:
            return updated_context
        else:
            raise HTTPException(status_code=404, detail="Context not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/ctxdb/contexts/query", response_model=list[Context])
def query_context(query: Context):
    try:
        query_ctx = Context(input=query.input, context=encode(query.input))
        # print(query_ctx)
        contexts = ctxdb.search_context(query_ctx, "context")
        # print(contexts)
        return contexts
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
