import os
from fastapi import FastAPI, HTTPException
from ctxdb.server.core import ContextDB
from ctxdb.common.models import InputContext, Context, OutputContext
from ctxdb.common.utils import encode
REDIS_HOST = os.environ["REDIS_HOST"]
REDIS_PORT = os.environ["REDIS_PORT"]
REDIS_PASSWORD = os.environ["REDIS_PASSWORD"]
app = FastAPI()
ctxdb = ContextDB()


@app.post("/ctxdb/contexts")
def add_context(input_ctx: InputContext):
    try:
        ctx = Context.from_orm(input_ctx)
        ctx.embedding = encode(ctx.text)
        # print(ctx)
        ctxdb.add_context(ctx)
        return {"message": "Context added successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/ctxdb/contexts/{idx}", response_model=OutputContext)
def get_context(idx: str):
    try:
        ctx = ctxdb.get_context(idx)
        return ctx
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.delete("/ctxdb/contexts/{idx}")
def delete_context(idx: str):
    try:
        ctxdb.delete_context(idx)
        return {"message": "Context deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))



@app.put("/ctxdb/contexts/{idx}")
def update_context(idx: str, input_ctx: InputContext):
    try:
        ctx = Context.from_orm(input_ctx)
        ctx.embedding = encode(input_ctx.text)
        ctxdb.update_context(idx, ctx)
        return {"message": "Context updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/ctxdb/contexts/query")
def query_context(input_ctx: InputContext):

    try:
        ctx = Context.from_orm(input_ctx)
        ctx.embedding = encode(input_ctx.text)
        contexts = ctxdb.search_context(ctx, "embedding")
        print(type(contexts))
        print(list(contexts.documents)[0].text)
        print(contexts.scores)
        return 200
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
