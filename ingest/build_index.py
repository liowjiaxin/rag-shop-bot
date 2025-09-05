import pandas as pd, json
from sentence_transformers import SentenceTransformer
import faiss
from pathlib import Path

EMB_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
INDEX_PATH = "data/faiss.index"
META_PATH  = "data/meta.jsonl"

def chunk_text(text, max_tokens=50, overlap=10):
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunks.append(" ".join(words[i:i+max_tokens]))
        i += max_tokens - overlap
    return chunks

# Load products
items = []
df = pd.read_csv("data/products.csv")
for _, r in df.iterrows():
    body = f"{r['title']} | {r['categories']} | {r['brand']} | {r['description']}"
    for c in chunk_text(body):
        items.append({"text": c, "source": "product", "id": str(r["id"]), "title": r["title"]})

# Load FAQs
faq_file = Path("data/faqs.md")
if faq_file.exists():
    txt = open(faq_file, "r", encoding="utf-8").read()
    for c in chunk_text(txt):
        items.append({"text": c, "source": "faqs", "id": "faqs", "title": "FAQs"})

# Build embeddings & FAISS index
model = SentenceTransformer(EMB_MODEL)
embs = model.encode([x["text"] for x in items], convert_to_numpy=True, normalize_embeddings=True)
index = faiss.IndexFlatIP(embs.shape[1])
index.add(embs)

faiss.write_index(index, INDEX_PATH)
with open(META_PATH, "w", encoding="utf-8") as f:
    for x in items:
        f.write(json.dumps(x, ensure_ascii=False) + "\n")

print("Index built with", len(items), "items")
