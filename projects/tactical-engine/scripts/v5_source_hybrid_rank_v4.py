"""Coverage-aware source selection for opt-in V5 heading reservation.

Keep semantic relevance as a gate, then prefer broader formation coverage only
among sources whose cross-encoder scores are close to the semantic winner.
No benchmark IDs, source names or formation lists are encoded here.
"""
from v5_source_semantic_rank_v3 import semantic_source_ranking


DEFAULT_SEMANTIC_MARGIN = 1.5


def select_source(question, rows, reranker, semantic_margin=DEFAULT_SEMANTIC_MARGIN):
    ranking = semantic_source_ranking(question, rows, reranker)
    if not ranking:
        return None, []
    best_score = ranking[0]["score"]
    traced = [
        {
            **item,
            "semantic_delta": best_score - item["score"],
            "competitive": best_score - item["score"] <= semantic_margin,
        }
        for item in ranking
    ]
    competitive = [item for item in traced if item["competitive"]]
    selected = sorted(
        competitive,
        key=lambda item: (-len(item["formations"]), -item["score"], item["source"]),
    )[0]
    return selected["source"], traced
