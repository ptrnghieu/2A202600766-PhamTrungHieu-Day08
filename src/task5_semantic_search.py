"""
Task 5 — Semantic Search Module.

Viết module tìm kiếm ngữ nghĩa (dense retrieval) trên vector store.

Implementation:
    - TF-IDF với cosine similarity (offline, không cần model download)
    - sublinear TF scaling + bigrams để capture context tốt hơn
    - Pre-built TF-IDF matrix từ Task 4

Yêu cầu:
    - Input: query string + top_k
    - Output: danh sách chunks có score, sorted descending
"""

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Lazy-loaded globals
_vectorizer = None
_tfidf_matrix = None
_chunks = None


def _load_resources() -> bool:
    """Load vectorizer và TF-IDF matrix (lazy, chỉ load lần đầu)."""
    global _vectorizer, _tfidf_matrix, _chunks

    if _vectorizer is not None and _chunks is not None:
        return True

    try:
        from src.task4_chunking_indexing import load_vectorstore
        _chunks, _vectorizer, _tfidf_matrix = load_vectorstore()
        return True
    except (FileNotFoundError, Exception):
        return False


def semantic_search(query: str, top_k: int = 10) -> list[dict]:
    """
    Tìm kiếm ngữ nghĩa sử dụng TF-IDF cosine similarity.

    Args:
        query: Câu truy vấn
        top_k: Số lượng kết quả tối đa

    Returns:
        List of {
            'content': str,      # Nội dung chunk
            'score': float,      # Cosine similarity score [0, 1]
            'metadata': dict     # source, doc_type, chunk_index
        }
        Sorted by score descending.
    """
    if not _load_resources():
        return []

    # Transform query với cùng vectorizer đã fit
    query_vector = _vectorizer.transform([query])

    # Cosine similarity giữa query và toàn bộ corpus
    similarities = cosine_similarity(query_vector, _tfidf_matrix).flatten()

    # Top-k indices sorted by score descending
    actual_k = min(top_k, len(_chunks))
    top_indices = np.argsort(similarities)[::-1][:actual_k]

    results = []
    for idx in top_indices:
        results.append({
            "content": _chunks[idx]["content"],
            "score": float(similarities[idx]),
            "metadata": _chunks[idx].get("metadata", {}),
        })

    return results


if __name__ == "__main__":
    results = semantic_search("hình phạt cho tội tàng trữ ma tuý", top_k=5)
    for r in results:
        print(f"[{r['score']:.3f}] {r['content'][:100]}...")
