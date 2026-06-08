"""
Task 7 — Reranking Module.

Phương pháp đã chọn:
    - Chính: Keyword-overlap reranking (không cần API, hoạt động offline)
    - Cũng implement: RRF (Reciprocal Rank Fusion) — dùng trong pipeline hybrid search

Giải thích RRF:
    RRF(d) = Σ_r 1 / (k + rank_r(d))
    - Gộp kết quả từ nhiều ranker (dense + sparse)
    - k=60 là hằng số làm mượt từ paper Cormack et al. 2009
    - Không phụ thuộc vào scale của score từ các ranker khác nhau

Giải thích Keyword-overlap reranker:
    - Tính tỷ lệ từ khóa trong query xuất hiện trong document
    - Kết hợp với original score: new_score = 0.6 * original + 0.4 * overlap
    - Tương tự BM25 nhưng đơn giản hơn, không cần index
"""


def rerank_cross_encoder(
    query: str, candidates: list[dict], top_k: int = 5
) -> list[dict]:
    """
    Rerank candidates sử dụng cross-encoder model.

    Thử Jina Reranker API nếu có JINA_API_KEY.
    Fallback sang keyword-overlap scoring nếu không có API key.
    """
    import os
    from dotenv import load_dotenv
    load_dotenv()

    jina_key = os.getenv("JINA_API_KEY", "")

    if jina_key and jina_key != "jina_xxx":
        try:
            import requests
            response = requests.post(
                "https://api.jina.ai/v1/rerank",
                headers={"Authorization": f"Bearer {jina_key}"},
                json={
                    "model": "jina-reranker-v2-base-multilingual",
                    "query": query,
                    "documents": [c["content"] for c in candidates],
                    "top_n": top_k,
                },
                timeout=10,
            )
            if response.ok:
                data = response.json().get("results", [])
                return [
                    {**candidates[r["index"]], "score": r["relevance_score"]}
                    for r in data[:top_k]
                ]
        except Exception:
            pass  # Fall through to keyword overlap

    # Fallback: keyword overlap reranker
    return _keyword_overlap_rerank(query, candidates, top_k)


def _keyword_overlap_rerank(
    query: str, candidates: list[dict], top_k: int = 5
) -> list[dict]:
    """
    Rerank bằng keyword overlap giữa query và document.
    Kết hợp với original score: 60% original + 40% keyword overlap.
    """
    query_terms = set(query.lower().split())
    rescored = []

    for c in candidates:
        content_terms = set(c["content"].lower().split())
        overlap = len(query_terms & content_terms) / max(len(query_terms), 1)
        original_score = c.get("score", 0.0)
        new_score = 0.6 * original_score + 0.4 * overlap
        rescored.append({**c, "score": new_score})

    rescored.sort(key=lambda x: x["score"], reverse=True)
    return rescored[:top_k]


def rerank_mmr(
    query_embedding,
    candidates: list[dict],
    top_k: int = 5,
    lambda_param: float = 0.7,
) -> list[dict]:
    """
    Maximal Marginal Relevance — vừa relevant vừa diverse.

    MMR = λ * sim(query, doc) - (1-λ) * max(sim(doc, selected_docs))

    Args:
        query_embedding: numpy array hoặc list
        candidates: List of {'content': str, 'score': float, 'embedding': list, 'metadata': dict}
        top_k: Số lượng kết quả
        lambda_param: Trade-off relevance (1.0) vs diversity (0.0)
    """
    import numpy as np

    if not candidates:
        return []

    def cosine_sim(a, b):
        a, b = np.array(a), np.array(b)
        denom = np.linalg.norm(a) * np.linalg.norm(b)
        return float(np.dot(a, b) / denom) if denom > 0 else 0.0

    selected_indices = []
    remaining_indices = list(range(len(candidates)))

    for _ in range(min(top_k, len(candidates))):
        best_idx = None
        best_score = float("-inf")

        for idx in remaining_indices:
            # Relevance to query
            emb = candidates[idx].get("embedding", None)
            if emb is not None:
                relevance = cosine_sim(query_embedding, emb)
            else:
                relevance = candidates[idx].get("score", 0.0)

            # Max similarity to already selected
            max_sim_to_selected = 0.0
            for sel_idx in selected_indices:
                sel_emb = candidates[sel_idx].get("embedding", None)
                curr_emb = candidates[idx].get("embedding", None)
                if sel_emb is not None and curr_emb is not None:
                    sim = cosine_sim(curr_emb, sel_emb)
                    max_sim_to_selected = max(max_sim_to_selected, sim)

            mmr_score = (
                lambda_param * relevance - (1 - lambda_param) * max_sim_to_selected
            )

            if mmr_score > best_score:
                best_score = mmr_score
                best_idx = idx

        if best_idx is not None:
            selected_indices.append(best_idx)
            remaining_indices.remove(best_idx)

    return [
        {**candidates[i], "score": candidates[i].get("score", 0.0)}
        for i in selected_indices
    ]


def rerank_rrf(
    ranked_lists: list[list[dict]], top_k: int = 5, k: int = 60
) -> list[dict]:
    """
    Reciprocal Rank Fusion — gộp kết quả từ nhiều ranker.

    RRF(d) = Σ 1 / (k + rank_r(d))

    Args:
        ranked_lists: List of ranked result lists (mỗi list từ 1 ranker)
        top_k: Số lượng kết quả cuối cùng
        k: Smoothing constant (default=60, từ paper Cormack et al. 2009)
    """
    rrf_scores: dict[str, float] = {}
    content_map: dict[str, dict] = {}

    for ranked_list in ranked_lists:
        for rank, item in enumerate(ranked_list, 1):
            key = item["content"]
            rrf_scores[key] = rrf_scores.get(key, 0.0) + 1.0 / (k + rank)
            content_map[key] = item

    sorted_items = sorted(rrf_scores.items(), key=lambda x: x[1], reverse=True)

    results = []
    for content, score in sorted_items[:top_k]:
        item = content_map[content].copy()
        item["score"] = score
        results.append(item)

    return results


def rerank(
    query: str,
    candidates: list[dict],
    top_k: int = 5,
    method: str = "keyword",
) -> list[dict]:
    """
    Unified reranking interface.

    Args:
        query: Câu truy vấn
        candidates: Danh sách candidates từ retrieval
        top_k: Số lượng kết quả sau rerank
        method: "keyword" | "cross_encoder" | "mmr" | "rrf"
    """
    if not candidates:
        return []

    if method == "keyword":
        return _keyword_overlap_rerank(query, candidates, top_k)
    elif method == "cross_encoder":
        return rerank_cross_encoder(query, candidates, top_k)
    elif method == "mmr":
        raise NotImplementedError("Call rerank_mmr with query_embedding")
    elif method == "rrf":
        raise NotImplementedError("Call rerank_rrf with ranked_lists")
    else:
        raise ValueError(f"Unknown rerank method: {method}")


if __name__ == "__main__":
    dummy_candidates = [
        {"content": "Điều 248: Tội tàng trữ trái phép chất ma tuý", "score": 0.8, "metadata": {}},
        {"content": "Nghệ sĩ X bị bắt vì sử dụng ma tuý", "score": 0.7, "metadata": {}},
        {"content": "Hình phạt tù từ 2-7 năm cho tội tàng trữ", "score": 0.6, "metadata": {}},
        {"content": "Python programming tips", "score": 0.4, "metadata": {}},
    ]
    results = rerank("hình phạt tàng trữ ma tuý", dummy_candidates, top_k=2)
    for r in results:
        print(f"[{r['score']:.3f}] {r['content']}")
