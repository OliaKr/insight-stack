
import redis
import json
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Connect to Redis
redis_client = redis.Redis(host="localhost", port=6379, decode_responses=True)

# Embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


def save_report_to_memory(key: str, text: str):
    vector = embedding_model.encode(text).tolist()
    record = {"text": text, "vector": vector}
    redis_client.rpush(key, json.dumps(record))


def retrieve_similar_memories(key: str, query: str, top_k: int = 3):
    query_vec = embedding_model.encode(query).reshape(1, -1)
    records = [json.loads(item) for item in redis_client.lrange(key, 0, -1)]

    if not records:
        return []

    vectors = np.array([r["vector"] for r in records])
    texts = [r["text"] for r in records]
    scores = cosine_similarity(query_vec, vectors)[0]
    ranked = sorted(zip(texts, scores), key=lambda x: x[1], reverse=True)

    return [text for text, _ in ranked[:top_k]]
