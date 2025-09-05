import json, faiss
from sentence_transformers import SentenceTransformer

EMB_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
INDEX_PATH = "data/faiss.index"
META_PATH  = "data/meta.jsonl"

class Retriever:
    def __init__(self, top_k=5):
        self.model = SentenceTransformer(EMB_MODEL)
        self.index = faiss.read_index(INDEX_PATH)
        self.meta = [json.loads(x) for x in open(META_PATH, "r", encoding="utf-8")]
        self.top_k = top_k

    def search(self, query):
        q_emb = self.model.encode([query], normalize_embeddings=True)
        scores, idxs = self.index.search(q_emb, self.top_k)
        results = []
        for i, score in zip(idxs[0], scores[0]):
            results.append((self.meta[i], float(score)))
        return results
