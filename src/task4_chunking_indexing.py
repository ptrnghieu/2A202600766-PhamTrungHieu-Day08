"""
Task 4 — Chunking & Indexing vào Vector Store.

Strategy lựa chọn:
    - Chunking: RecursiveCharacterTextSplitter (safe default, handles Vietnamese well)
    - Embedding: TF-IDF với sublinear scaling (offline, không cần download model)
    - Vector Store: numpy + pickle (zero-dependency local store, no server needed)

Lý do chọn RecursiveCharacterTextSplitter:
    - Tự động dùng separator phù hợp nhất (paragraph > newline > sentence > word)
    - Phù hợp với cả văn bản pháp luật (có cấu trúc) và bài báo (tự do)

Lý do chọn TF-IDF:
    - Chạy hoàn toàn offline, không cần download model
    - sublinear_tf=True giảm ảnh hưởng của từ xuất hiện quá nhiều
    - max_features=10000 cho tiếng Việt với nhiều từ đặc thù pháp luật

Cài đặt:
    pip install langchain-text-splitters scikit-learn numpy
"""

import pickle
from pathlib import Path

import numpy as np

STANDARDIZED_DIR = Path(__file__).parent.parent / "data" / "standardized"
VECTORSTORE_DIR = Path(__file__).parent.parent / "data" / "vectorstore"

# =============================================================================
# CONFIGURATION — Giải thích lựa chọn ở trên
# =============================================================================

# CHUNK_SIZE=500: Đủ để chứa 1 điều luật hoặc 2-3 đoạn văn.
# Nhỏ hơn sẽ mất context; lớn hơn gây lost-in-the-middle khi inject vào LLM.
CHUNK_SIZE = 500

# CHUNK_OVERLAP=50: ~10% overlap giữ liên kết ngữ nghĩa giữa các chunk.
CHUNK_OVERLAP = 50

CHUNKING_METHOD = "recursive"  # RecursiveCharacterTextSplitter

# TF-IDF: offline, no download needed, sublinear TF scaling
EMBEDDING_MODEL = "tfidf"
EMBEDDING_DIM = 10000  # max_features


# =============================================================================
# IMPLEMENTATION
# =============================================================================

def load_documents() -> list[dict]:
    """
    Đọc toàn bộ markdown files từ data/standardized/.

    Returns:
        List of {'content': str, 'metadata': {'source': str, 'type': str}}
    """
    documents = []
    for md_file in STANDARDIZED_DIR.rglob("*.md"):
        content = md_file.read_text(encoding="utf-8")
        if not content.strip():
            continue
        doc_type = "legal" if "legal" in str(md_file) else "news"
        documents.append({
            "content": content,
            "metadata": {
                "source": md_file.name,
                "type": doc_type,
                "path": str(md_file),
            }
        })
    return documents


def chunk_documents(documents: list[dict]) -> list[dict]:
    """
    Chunk documents bằng RecursiveCharacterTextSplitter.

    Returns:
        List of {'content': str, 'metadata': dict} — mỗi item là 1 chunk
    """
    from langchain_text_splitters import RecursiveCharacterTextSplitter

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", " ", ""],
    )

    chunks = []
    for doc in documents:
        splits = splitter.split_text(doc["content"])
        for i, chunk_text in enumerate(splits):
            if chunk_text.strip():
                chunks.append({
                    "content": chunk_text,
                    "metadata": {**doc["metadata"], "chunk_index": i},
                })
    return chunks


def embed_chunks(chunks: list[dict]):
    """
    Embed toàn bộ chunks bằng TF-IDF (offline, no download needed).

    Returns:
        (vectorizer, tfidf_matrix) — sparse matrix shape (num_chunks, max_features)
    """
    from sklearn.feature_extraction.text import TfidfVectorizer

    texts = [c["content"] for c in chunks]
    vectorizer = TfidfVectorizer(
        max_features=EMBEDDING_DIM,
        sublinear_tf=True,
        ngram_range=(1, 2),
    )
    tfidf_matrix = vectorizer.fit_transform(texts)
    return vectorizer, tfidf_matrix


def index_to_vectorstore(chunks: list[dict], vectorizer, tfidf_matrix):
    """
    Lưu chunks, vectorizer và TF-IDF matrix vào local vector store.
    """
    VECTORSTORE_DIR.mkdir(parents=True, exist_ok=True)

    chunks_path = VECTORSTORE_DIR / "chunks.pkl"
    vectorizer_path = VECTORSTORE_DIR / "vectorizer.pkl"
    matrix_path = VECTORSTORE_DIR / "tfidf_matrix.pkl"

    with open(chunks_path, "wb") as f:
        pickle.dump(chunks, f)

    with open(vectorizer_path, "wb") as f:
        pickle.dump(vectorizer, f)

    with open(matrix_path, "wb") as f:
        pickle.dump(tfidf_matrix, f)

    print(f"✓ Saved {len(chunks)} chunks to {VECTORSTORE_DIR}")


def load_vectorstore():
    """
    Load pre-built vector store từ disk.

    Returns:
        (chunks, vectorizer, tfidf_matrix)
    """
    chunks_path = VECTORSTORE_DIR / "chunks.pkl"
    vectorizer_path = VECTORSTORE_DIR / "vectorizer.pkl"
    matrix_path = VECTORSTORE_DIR / "tfidf_matrix.pkl"

    if not chunks_path.exists() or not vectorizer_path.exists():
        raise FileNotFoundError(
            f"Vector store not found at {VECTORSTORE_DIR}. "
            "Run task4_chunking_indexing.run_pipeline() first."
        )

    with open(chunks_path, "rb") as f:
        chunks = pickle.load(f)

    with open(vectorizer_path, "rb") as f:
        vectorizer = pickle.load(f)

    with open(matrix_path, "rb") as f:
        tfidf_matrix = pickle.load(f)

    return chunks, vectorizer, tfidf_matrix


def run_pipeline():
    """Chạy toàn bộ pipeline: load → chunk → embed → index."""
    print("=" * 50)
    print("Task 4: Chunking & Indexing")
    print(f"  Chunking: {CHUNKING_METHOD} (size={CHUNK_SIZE}, overlap={CHUNK_OVERLAP})")
    print(f"  Embedding: {EMBEDDING_MODEL} (dim={EMBEDDING_DIM})")
    print(f"  Vector Store: numpy/pickle")
    print("=" * 50)

    docs = load_documents()
    print(f"\n✓ Loaded {len(docs)} documents")

    if not docs:
        print("⚠ No documents found. Run Tasks 1-3 first.")
        return

    chunks = chunk_documents(docs)
    print(f"✓ Created {len(chunks)} chunks")

    print("Embedding with TF-IDF (offline, no download needed)...")
    vectorizer, tfidf_matrix = embed_chunks(chunks)
    print(f"✓ TF-IDF matrix shape: {tfidf_matrix.shape}")

    index_to_vectorstore(chunks, vectorizer, tfidf_matrix)
    print("✓ Indexed to vector store")


if __name__ == "__main__":
    run_pipeline()
