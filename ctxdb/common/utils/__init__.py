from sentence_transformers import SentenceTransformer

transformer = SentenceTransformer('all-MiniLM-L6-v2')


def encode(text):
    return transformer.encode(text)
