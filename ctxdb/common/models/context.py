from docarray import BaseDoc, DocList
from docarray.typing import AnyEmbedding, NdArray
from docarray.documents import TextDoc, ImageDoc, AudioDoc, VideoDoc
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
    confidence: Optional[float]
    class Config:
        orm_mode = True

class BaseContext(BaseDoc):
    input: str
    output: Optional[str]

class FullContext(BaseContext):
    texts: Optional[DocList[TextDoc]]
    images: Optional[DocList[ImageDoc]]
    audios: Optional[DocList[AudioDoc]]
    videos: Optional[DocList[VideoDoc]]

class ContextList(DocList):
    class Config:
        orm_mode = True


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
