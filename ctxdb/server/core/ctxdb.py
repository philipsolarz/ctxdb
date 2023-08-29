# from ..models import Namespace, Workspace, Context
from ctxdb.common.models import Context
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
                self._ctx_idx = InMemoryExactNNIndex[Context]()
            except ImportError:
                raise ImportError(
                    "Please install docarray[index] to use ContextDB")
        elif db_type == "redis":
            try:
                from docarray.index import RedisDocumentIndex
                self._ctx_idx = RedisDocumentIndex[Context](
                    host=host,
                    port=port,
                    password=password)
            except ImportError:
                raise ImportError(
                    "Please install docarray[redis] to use ContextDB")
        else:
            raise NotImplementedError(f"{db_type} is not supported")

    def add_context(self, ctx: Context):
        if isinstance(ctx, Context):
            self._ctx_idx.index(ctx)
        else:
            raise TypeError(f"{type(ctx)} is not supported")

    def get_context(self, ctx_id: str):
        if isinstance(ctx_id, str):
            return self._ctx_idx[ctx_id]
        else:
            raise TypeError(f"{type(ctx_id)} is not supported")

    def delete_context(self, ctx_id: str):
        if isinstance(ctx_id, str):
            del self._ctx_idx[ctx_id]
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
            return self._ctx_idx.find(ctx.embedding, search_field, limit)
        else:
            raise TypeError(f"{type(ctx)} is not supported")