"""
Task 10 — Generation Có Citation.

Hướng dẫn:
    1. Chọn top_k, top_p phù hợp (giải thích lý do)
    2. Sắp xếp lại chunks sau reranking để tránh "lost in the middle"
    3. Inject context vào prompt
    4. Yêu cầu LLM trả lời có citation
    5. Nếu không đủ evidence → "I cannot verify this information"
"""

import os

from dotenv import load_dotenv

load_dotenv()

from .task9_retrieval_pipeline import retrieve


# =============================================================================
# CONFIGURATION — Giải thích lựa chọn
# =============================================================================

# TOP_K=5: Đủ context, tránh quá dài gây "lost in the middle".
# Theo nghiên cứu Liu et al. 2023, LLM nhớ tốt thông tin ở đầu và cuối prompt.
TOP_K = 5

# TOP_P=0.9 (nucleus sampling): Đảm bảo diversity mà không quá random.
# Cho RAG factual nên giữ top_p < 1.0 để tránh hallucination.
TOP_P = 0.9

# TEMPERATURE=0.3: RAG cần câu trả lời factual, ít sáng tạo.
# Giá trị thấp giảm hallucination, tăng bám sát context.
TEMPERATURE = 0.3


# =============================================================================
# SYSTEM PROMPT
# =============================================================================

SYSTEM_PROMPT = """Answer the following question comprehensively in Vietnamese.
For every statement of fact or claim, immediately insert a citation in brackets
linking to the specific source (e.g., [Luật Phòng chống ma tuý 2021, Điều 3]
or [VnExpress, 2024]).

If the information is not explicitly stated in the provided context or knowledge
base, state 'Tôi không thể xác minh thông tin này từ nguồn hiện có' rather than
guessing.

Rules:
- Only use information from the provided context
- Every factual claim MUST have a citation
- If context is insufficient, say so clearly
- Structure your answer with clear paragraphs"""


# =============================================================================
# DOCUMENT REORDERING (tránh lost in the middle)
# =============================================================================

def reorder_for_llm(chunks: list[dict]) -> list[dict]:
    """
    Sắp xếp chunks để tránh "lost in the middle" effect.

    LLM nhớ tốt thông tin ở ĐẦU và CUỐI prompt, quên thông tin ở GIỮA.
    Strategy: chunk quan trọng nhất (rank 0) ở đầu,
              chunk quan trọng nhì (rank 1) ở cuối,
              các chunk còn lại ở giữa theo thứ tự tăng dần về tầm quan trọng.

    Input order (by score):  [0, 1, 2, 3, 4]
    Output order:            [0, 2, 4, 3, 1]
    (best → đầu; second-best → cuối; rest → giữa)

    Args:
        chunks: List sorted by score descending (from retrieval)

    Returns:
        List reordered để maximize LLM attention.
    """
    if len(chunks) <= 2:
        return chunks

    # Split: even-indexed go to front (odd positions), odd-indexed to back (reversed)
    front = chunks[0::2]   # Index 0, 2, 4, ... (most → least important at front)
    back = chunks[1::2]    # Index 1, 3, 5, ... (second → least important at back)
    back_reversed = list(reversed(back))  # Least important in middle, second-best at end

    # First chunk (most important) must stay at position 0
    reordered = front[:1] + back_reversed[1:] + [back_reversed[0]] if back_reversed else front

    # Safety: ensure we don't lose chunks
    if len(reordered) != len(chunks):
        return chunks

    return reordered


# =============================================================================
# CONTEXT FORMATTING
# =============================================================================

def format_context(chunks: list[dict]) -> str:
    """
    Format chunks thành context string cho prompt.
    Mỗi chunk có label source để LLM có thể cite.

    Args:
        chunks: List of {'content': str, 'metadata': dict, 'score': float}

    Returns:
        Formatted context string.
    """
    context_parts = []
    for i, chunk in enumerate(chunks, 1):
        metadata = chunk.get("metadata", {})
        source = metadata.get("source", f"Source {i}")
        doc_type = metadata.get("type", "unknown")
        # Keep original filename for citations; strip only the .md extension
        source_display = source.replace(".md", "") if source.endswith(".md") else source

        context_parts.append(
            f"[Document {i} | Source: {source_display} | Type: {doc_type}]\n"
            f"{chunk['content']}\n"
        )

    return "\n---\n".join(context_parts)


# =============================================================================
# GENERATION
# =============================================================================

def generate_with_citation(query: str, top_k: int = TOP_K) -> dict:
    """
    End-to-end RAG generation có citation.

    Pipeline:
        1. Retrieve relevant chunks (Task 9)
        2. Reorder để tránh lost in the middle
        3. Format context với source labels
        4. Build prompt (system + context + query)
        5. Call LLM (OpenAI API hoặc fallback nếu không có key)
        6. Return answer + sources

    Args:
        query: Câu hỏi của user
        top_k: Số chunks đưa vào context

    Returns:
        {
            'answer': str,           # Câu trả lời có citation
            'sources': list[dict],   # Các chunks đã dùng
            'retrieval_source': str  # 'hybrid' hoặc 'pageindex'
        }
    """
    # Step 1: Retrieve
    chunks = retrieve(query, top_k=top_k)

    if not chunks:
        return {
            "answer": "Tôi không thể xác minh thông tin này từ nguồn hiện có.",
            "sources": [],
            "retrieval_source": "none",
        }

    # Step 2: Reorder để tránh lost in the middle
    reordered = reorder_for_llm(chunks)

    # Step 3: Format context với source labels
    context = format_context(reordered)

    # Step 4: Build prompt
    user_message = f"Context:\n{context}\n\n---\n\nQuestion: {query}"

    retrieval_source = chunks[0].get("source", "hybrid") if chunks else "none"

    # Step 5: Call LLM
    openai_key = os.getenv("OPENAI_API_KEY", "")

    if openai_key and openai_key != "sk-xxx":
        answer = _call_openai(user_message, openai_key)
    else:
        # Fallback: trả lời dựa trên context mà không cần LLM API
        answer = _fallback_answer(query, reordered)

    return {
        "answer": answer,
        "sources": chunks,
        "retrieval_source": retrieval_source,
    }


def _call_openai(user_message: str, api_key: str) -> str:
    """Gọi OpenAI API để generate câu trả lời."""
    from openai import OpenAI

    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
        temperature=TEMPERATURE,
        top_p=TOP_P,
    )
    return response.choices[0].message.content


def _fallback_answer(query: str, chunks: list[dict]) -> str:
    """
    Fallback khi không có OpenAI API key.
    Trả lời đơn giản dựa trên các chunks đã retrieve.
    """
    if not chunks:
        return "Tôi không thể xác minh thông tin này từ nguồn hiện có."

    lines = [f"Dựa trên các tài liệu pháp luật và tin tức được cung cấp:\n"]

    for i, chunk in enumerate(chunks[:3], 1):
        metadata = chunk.get("metadata", {})
        source = metadata.get("source", f"Tài liệu {i}").replace(".md", "")
        lines.append(f"• [{source}]: {chunk['content'][:300]}...\n")

    lines.append(
        "\n(Lưu ý: Câu trả lời này được tạo từ retrieval trực tiếp, "
        "không qua LLM. Vui lòng set OPENAI_API_KEY để nhận câu trả lời "
        "đầy đủ có citation.)"
    )

    return "\n".join(lines)


if __name__ == "__main__":
    test_queries = [
        "Hình phạt cho tội tàng trữ trái phép chất ma tuý theo pháp luật Việt Nam?",
        "Những nghệ sĩ nào đã bị bắt vì liên quan tới ma tuý?",
        "Quy trình cai nghiện bắt buộc theo Luật Phòng chống ma tuý 2021?",
    ]

    for q in test_queries:
        print(f"\n{'='*70}")
        print(f"Q: {q}")
        print("=" * 70)
        result = generate_with_citation(q)
        print(f"\nA: {result['answer']}")
        print(f"\n[Sources: {len(result['sources'])} chunks | via {result['retrieval_source']}]")
