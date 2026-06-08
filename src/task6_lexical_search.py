"""
Task 6 — Lexical Search Module (BM25).

Mặc định sử dụng BM25. Nếu dùng phương pháp khác (TF-IDF, Elasticsearch,
Weaviate BM25 built-in), hãy giải thích cơ chế trong buổi demo → +5 bonus.

Cài đặt:
    pip install rank-bm25

BM25 hoạt động thế nào:
    - Term Frequency (TF): từ xuất hiện nhiều trong document → điểm cao
    - Inverse Document Frequency (IDF): từ hiếm → quan trọng hơn
    - Document length normalization: document dài không bị ưu tiên quá mức
    - Formula: score(q,d) = Σ IDF(qi) * (tf(qi,d) * (k1+1)) / (tf(qi,d) + k1*(1-b+b*|d|/avgdl))
    - k1=1.5 (term saturation), b=0.75 (length normalization)
"""

import numpy as np

# Lazy-loaded BM25 index
_bm25 = None
_corpus: list[dict] = []


def _load_corpus():
    """Load corpus từ vector store (lazy)."""
    global _corpus
    if _corpus:
        return True
    try:
        from src.task4_chunking_indexing import load_vectorstore
        chunks, _vectorizer, _matrix = load_vectorstore()
        _corpus = chunks
        return True
    except (FileNotFoundError, Exception):
        return False


def build_bm25_index(corpus: list[dict]):
    """
    Xây dựng BM25 index từ corpus.

    Args:
        corpus: List of {'content': str, 'metadata': dict}

    Returns:
        BM25Okapi instance
    """
    from rank_bm25 import BM25Okapi

    # Tokenize — simple split for Vietnamese (no word segmentation needed for BM25)
    tokenized_corpus = [doc["content"].lower().split() for doc in corpus]
    return BM25Okapi(tokenized_corpus)


def _get_bm25():
    """Get or build BM25 index (lazy)."""
    global _bm25, _corpus

    if _bm25 is not None:
        return _bm25, _corpus

    if not _load_corpus():
        return None, []

    _bm25 = build_bm25_index(_corpus)
    return _bm25, _corpus


def lexical_search(query: str, top_k: int = 10) -> list[dict]:
    """
    Tìm kiếm từ khóa sử dụng BM25.

    Args:
        query: Câu truy vấn
        top_k: Số lượng kết quả tối đa

    Returns:
        List of {
            'content': str,
            'score': float,      # BM25 score
            'metadata': dict
        }
        Sorted by score descending.
    """
    bm25, corpus = _get_bm25()

    if bm25 is None or not corpus:
        return []

    tokenized_query = query.lower().split()
    scores = bm25.get_scores(tokenized_query)

    # Get top_k indices sorted by score descending
    actual_k = min(top_k, len(corpus))
    top_indices = np.argsort(scores)[::-1][:actual_k]

    results = []
    for idx in top_indices:
        if scores[idx] > 0:
            results.append({
                "content": corpus[idx]["content"],
                "score": float(scores[idx]),
                "metadata": corpus[idx].get("metadata", {}),
            })

    # If no results with score > 0, return top_k anyway
    if not results:
        for idx in top_indices:
            results.append({
                "content": corpus[idx]["content"],
                "score": float(scores[idx]),
                "metadata": corpus[idx].get("metadata", {}),
            })

    return results[:top_k]


if __name__ == "__main__":
    results = lexical_search("Điều 248 tàng trữ trái phép chất ma tuý", top_k=5)
    for r in results:
        print(f"[{r['score']:.3f}] {r['content'][:100]}...")
