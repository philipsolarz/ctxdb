from docarray import BaseDoc
from docarray.typing import AnyEmbedding, NdArray
from docarray.documents import TextDoc
from docarray import DocList
from docarray.typing.url import TextUrl
from typing import Optional

class InputContext(TextDoc):
    class Config:
        orm_mode = True
class Context(TextDoc):
    class Config:
        orm_mode = True
    # context: Optional[NdArray[384]]
    
class OutputContext(TextDoc):
    class Config:
        orm_mode = True

class BaseContext(BaseDoc):
    input: str
    output: Optional[str]




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
