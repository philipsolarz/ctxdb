from docarray import BaseDoc
from docarray.typing import AnyEmbedding, NdArray
from docarray.documents import TextDoc
from docarray import DocList
from typing import Optional


class BaseContext(BaseDoc):
    input: str
    output: str


class Context(BaseContext):
    context: NdArray[384]

"""



class QueryContext(BaseDoc):
    query: AnyEmbedding[512]
    input: AnyEmbedding[512]
    context: AnyEmbedding[512]
    output: TextDoc


class InstructContext(BaseDoc):
    instructions: AnyEmbedding[512]
    input: AnyEmbedding[512]
    context: AnyEmbedding[512]
    output: TextDoc


class Context(BaseDoc):
    namespace: str
    workspace: str
    ctx_id: str
    embedding: AnyEmbedding[512]
"""
