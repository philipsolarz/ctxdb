# from ..models import Namespace, Workspace, Context

from ctxdb.common.models import Context, Contexts
# from ctxdb.server.core.config import settings
# from docarray.index import RedisDocumentIndex, InMemoryExactNNIndex
# from docarray.index import InMemoryExactNNIndex
#from ctxdb.transformers import transformer
# from docarray import DocList
#from typing import List


class ContextDB:

    def __init__(self, db_type: str = "in_memory", host: str = "localhost", port: int = 6379, password: str = None):
        self.setup_backend(db_type, host, port, password)
        print("Hello World")

    def setup_backend(self, db_type, host, port, password):
        if db_type == "in_memory":
            try:
                from docarray.index import InMemoryExactNNIndex
                self.db = InMemoryExactNNIndex[Context]()
            except ImportError:
                raise ImportError(
                    "Please install docarray[index] to use ContextDB")
        elif db_type == "redis":
            try:
                from docarray.index import RedisDocumentIndex
                self.db = RedisDocumentIndex[Context](
                    host=host,
                    port=port,
                    password=password)
            except ImportError:
                raise ImportError(
                    "Please install docarray[redis] to use ContextDB")
        else:
            raise NotImplementedError(f"{db_type} is not supported")

    def add_contexts(self, cxts: Contexts):
        if isinstance(cxts, Contexts):
            self.db.index(cxts)
        else:
            raise TypeError(f"{type(cxts)} is not supported")
        
    def add_context(self, ctx: Context):
        if isinstance(ctx, Context):
            self.db.index(ctx)
        else:
            raise TypeError(f"{type(ctx)} is not supported")

    def get_context(self, ctx_id: str):
        if isinstance(ctx_id, str):
            return self.db[ctx_id]
        else:
            raise TypeError(f"{type(ctx_id)} is not supported")

    def delete_context(self, ctx_id: str):
        if isinstance(ctx_id, str):
            del self.db[ctx_id]
        else:
            raise TypeError(f"{type(ctx_id)} is not supported")

    def update_context(self, ctx_id: str, ctx: Context):
        pass

    def search_context(self,
                       ctx: Context,
                       search_field: str = "embedding",
                       limit: int = 10):
        # print(ctx)
        if isinstance(ctx, Context):
            return self.db.find(ctx.embedding, search_field, limit)
        else:
            raise TypeError(f"{type(ctx)} is not supported")
        
    def find_contexts(self, cxts: Contexts, search_field: str = "embedding", limit: int = 10):
        if isinstance(cxts, Contexts):
            return self.db.find_batched(cxts, search_field, limit)
        else:
            raise TypeError(f"{type(cxts)} is not supported")
        
    def filter(self, query):
        return self.db.filter(query)
    
    def advanced_search(self, query):
        query = (self.db.build_query())
        return self.db.execute_query(query)