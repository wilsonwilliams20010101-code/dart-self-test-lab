from __future__ import annotations
import random
from typing import List, Dict, Any, Optional

def pick_questions(all_qs: List[Dict[str, Any]], n: int = 5, category: Optional[str] = None) -> List[Dict[str, Any]]:
    pool = [q for q in all_qs if (category is None or q.get("category")==category)]
    random.shuffle(pool)
    return pool[:n]

def score_quiz(questions: List[Dict[str, Any]], answers: List[int]) -> int:
    score = 0
    for q, a in zip(questions, answers):
        if a is not None and a == q.get("answer_index"):
            score += 1
    return score
