import os
import logging
from fastapi import FastAPI, HTTPException, Depends
from ctxdb.server.core import ContextDB
from ctxdb.common.models import InputContext, Context, OutputContext, ContextList
from ctxdb.common.utils import encode
from config import setup_logger
from typing import List
from docarray.base_doc import DocArrayResponse
from docarray import DocList
logger = setup_logger()

def encode_context(input_ctx: InputContext) -> Context:
    """Encode the text and create a Context instance from an InputContext instance.
    
    Args:
        input_ctx (InputContext): Input context to encode.
    
    Returns:
        Context: Encoded context.
    """
    ctx = Context.from_orm(input_ctx)
    print(ctx)
    ctx.embedding = encode(ctx.text)

    return ctx

def setup_routes(api: FastAPI, ctxdb: ContextDB) -> None:
    @api.post("/ctxdb/contexts", response_model=dict)
    def add_context(input_ctx: InputContext) -> dict:
        """Add a new context.
        
        Args:
            input_ctx (InputContext): Context to add.
            ctxdb (ContextDB): Database instance.
        
        Returns:
            dict: Message.
        """
        try:
            ctx = encode_context(input_ctx)
            ctxdb.add_context(ctx)
            return {"message": "Context added successfully"}
        except Exception as e:
            logger.error(f"Error in adding context: {e}")
            raise HTTPException(status_code=400, detail=str(e))

    @api.get("/ctxdb/contexts/{idx}", response_model=OutputContext)
    def get_context(idx: str) -> OutputContext:
        """Get a context by its index.
        
        Args:
            idx (str): Index of the context to retrieve.
            ctxdb (ContextDB): Database instance.
        
        Returns:
            OutputContext: The requested context.
        """
        try:
            return ctxdb.get_context(idx)
        except Exception as e:
            logger.error(f"Error in getting context: {e}")
            raise HTTPException(status_code=400, detail=str(e))

    @api.delete("/ctxdb/contexts/{idx}", response_model=dict)
    def delete_context(idx: str) -> dict:
        """Delete a context by its index.
        
        Args:
            idx (str): Index of the context to delete.
            ctxdb (ContextDB): Database instance.
        
        Returns:
            dict: Message.
        """
        try:
            ctxdb.delete_context(idx)
            return {"message": "Context deleted successfully"}
        except Exception as e:
            logger.error(f"Error in deleting context: {e}")
            raise HTTPException(status_code=400, detail=str(e))

    @api.put("/ctxdb/contexts/{idx}", response_model=dict)
    def update_context(idx: str, input_ctx: InputContext) -> dict:
        """Update an existing context by its index.
        
        Args:
            idx (str): Index of the context to update.
            input_ctx (InputContext): New context information.
            ctxdb (ContextDB): Database instance.
        
        Returns:
            dict: Message.
        """
        try:
            ctx = encode_context(input_ctx)
            ctxdb.update_context(idx, ctx)
            return {"message": "Context updated successfully"}
        except Exception as e:
            logger.error(f"Error in updating context: {e}")
            raise HTTPException(status_code=400, detail=str(e))

    @api.post("/ctxdb/contexts/query", response_model=List[OutputContext], response_class=DocArrayResponse)
    def query_context(input_ctx: InputContext) -> List[OutputContext]:
        """Query for a context.
        
        Args:
            input_ctx (InputContext): Context to query.
            ctxdb (ContextDB): Database instance.
        
        Returns:
            int: HTTP status code.
        """
        try:
            ctx = encode_context(input_ctx)
            results = DocList[OutputContext]()
            contexts, scores = ctxdb.search_context(ctx, "embedding", 3)
            for ctx, score in zip(contexts, scores):
                result = OutputContext.from_orm(ctx)
                result.confidence = score
                result.embedding = None
                results.append(doc=result)
            print(f"Contexts: {results.url}, Confidence: {results.confidence}")
            return results
        except Exception as e:
            logger.error(f"Error in querying context: {e}")
            raise HTTPException(status_code=400, detail=str(e))
