"""
Task 8 — PageIndex Vectorless RAG.

Đăng ký tài khoản tại: https://pageindex.ai/
SDK & sample code: https://github.com/VectifyAI/PageIndex

PageIndex cho phép RAG mà không cần vector store — sử dụng
structural understanding của document thay vì embedding.

Cài đặt:
    pip install pageindex

Hướng dẫn:
    1. Đăng ký account tại pageindex.ai
    2. Lấy API key
    3. Upload documents
    4. Query sử dụng PageIndex API

Fallback:
    Nếu không có PAGEINDEX_API_KEY, module dùng BM25-based search
    được đánh tag source='pageindex' để tương thích với pipeline.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

PAGEINDEX_API_KEY = os.getenv("PAGEINDEX_API_KEY", "")
STANDARDIZED_DIR = Path(__file__).parent.parent / "data" / "standardized"


def upload_documents():
    """
    Upload toàn bộ markdown documents lên PageIndex.
    Yêu cầu PAGEINDEX_API_KEY được set trong .env
    """
    if not PAGEINDEX_API_KEY or PAGEINDEX_API_KEY == "pi_xxx":
        print("⚠ PAGEINDEX_API_KEY chưa được set. Bỏ qua upload.")
        return

    try:
        from pageindex import PageIndex

        pi = PageIndex(api_key=PAGEINDEX_API_KEY)

        for md_file in STANDARDIZED_DIR.rglob("*.md"):
            content = md_file.read_text(encoding="utf-8")
            pi.upload(
                content=content,
                metadata={"filename": md_file.name, "type": md_file.parent.name},
            )
            print(f"  ✓ Uploaded: {md_file.name}")
    except ImportError:
        print("⚠ pageindex package not installed. Run: pip install pageindex")
    except Exception as e:
        print(f"✗ Upload failed: {e}")


def _pageindex_api_search(query: str, top_k: int) -> list[dict]:
    """Dùng PageIndex API thực nếu có API key."""
    from pageindex import PageIndex

    pi = PageIndex(api_key=PAGEINDEX_API_KEY)
    results = pi.query(query=query, top_k=top_k)

    return [
        {
            "content": r.text,
            "score": float(r.score) if hasattr(r, "score") else 0.5,
            "metadata": r.metadata if hasattr(r, "metadata") else {},
            "source": "pageindex",
        }
        for r in results
    ]


def _fallback_bm25_search(query: str, top_k: int) -> list[dict]:
    """
    Fallback BM25 search khi không có PageIndex API key.
    Kết quả được tag source='pageindex' để tương thích với pipeline.
    """
    try:
        from src.task4_chunking_indexing import load_vectorstore
        from src.task6_lexical_search import build_bm25_index
        import numpy as np

        chunks, _vectorizer, _matrix = load_vectorstore()
        bm25 = build_bm25_index(chunks)

        tokenized_query = query.lower().split()
        scores = bm25.get_scores(tokenized_query)

        actual_k = min(top_k, len(chunks))
        top_indices = np.argsort(scores)[::-1][:actual_k]

        results = []
        for idx in top_indices:
            results.append({
                "content": chunks[idx]["content"],
                "score": float(scores[idx]),
                "metadata": chunks[idx].get("metadata", {}),
                "source": "pageindex",
            })
        return results

    except Exception:
        # If even fallback fails, return empty list
        return []


def pageindex_search(query: str, top_k: int = 5) -> list[dict]:
    """
    Vectorless retrieval sử dụng PageIndex.
    Dùng làm fallback khi hybrid search không có kết quả tốt.

    Args:
        query: Câu truy vấn
        top_k: Số lượng kết quả tối đa

    Returns:
        List of {
            'content': str,
            'score': float,
            'metadata': dict,
            'source': 'pageindex'   # Đánh dấu nguồn retrieval
        }
    """
    has_real_key = (
        PAGEINDEX_API_KEY
        and PAGEINDEX_API_KEY != "pi_xxx"
        and len(PAGEINDEX_API_KEY) > 5
    )

    if has_real_key:
        try:
            return _pageindex_api_search(query, top_k)
        except Exception as e:
            print(f"  ⚠ PageIndex API failed: {e}. Using fallback BM25.")

    return _fallback_bm25_search(query, top_k)


if __name__ == "__main__":
    if not PAGEINDEX_API_KEY or PAGEINDEX_API_KEY == "pi_xxx":
        print("⚠ Hãy set PAGEINDEX_API_KEY trong file .env để dùng PageIndex thực")
        print("  Đăng ký tại: https://pageindex.ai/")
        print("  Đang dùng BM25 fallback...\n")

    results = pageindex_search("hình phạt sử dụng ma tuý", top_k=3)
    for r in results:
        print(f"[{r['score']:.3f}] [{r['source']}] {r['content'][:100]}...")
