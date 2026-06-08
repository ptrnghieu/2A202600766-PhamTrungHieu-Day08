"""
Local index utilities.

Cung cấp tokenizer đơn giản cho tiếng Việt và helper load chunks từ vectorstore
để dùng trong evaluation pipeline mà không cần import phức tạp.
"""

import re
from typing import Any

# Cache để tránh load lại nhiều lần
_chunks_cache: list[dict] | None = None


def tokenize(text: str) -> list[str]:
    """
    Tokenize tiếng Việt đơn giản: tách theo khoảng trắng và dấu câu.

    Đủ dùng cho overlap-based metrics trong eval pipeline khi không có RAGAS.

    Args:
        text: Văn bản tiếng Việt cần tokenize.

    Returns:
        List các token lowercase.
    """
    return re.findall(r"\w+", text.lower())


def ensure_chunks(force_reload: bool = False) -> list[dict]:
    """
    Load chunks từ vectorstore, cache sau lần đầu.

    Dùng trong eval pipeline và golden_dataset_tools để sample context
    khi generate Q&A candidates.

    Args:
        force_reload: Nếu True, bỏ qua cache và load lại.

    Returns:
        List of {'content': str, 'metadata': dict} chunks.
    """
    global _chunks_cache

    if _chunks_cache is not None and not force_reload:
        return _chunks_cache

    try:
        from src.task4_chunking_indexing import load_vectorstore
        chunks, _vectorizer, _matrix = load_vectorstore()
        _chunks_cache = chunks
        return chunks
    except Exception:
        # Fallback: load trực tiếp từ pickle nếu có
        try:
            import pickle
            from pathlib import Path
            chunks_path = Path(__file__).parent.parent / "data" / "vectorstore" / "chunks.pkl"
            with open(chunks_path, "rb") as f:
                _chunks_cache = pickle.load(f)
            return _chunks_cache
        except Exception:
            return []
