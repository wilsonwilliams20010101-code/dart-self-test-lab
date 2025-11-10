import random

def pick_questions(qs_all, n=5, category=None):
    if not qs_all:
        return []
    pool = [q for q in qs_all if (category is None or q.get("category","General")==category)]
    random.shuffle(pool)
    return pool[:n]

def score_quiz(questions, answers):
    score = 0
    for q, a in zip(questions, answers):
        if a == q.get("answer_index", 0):
            score += 1
    return score