from __future__ import annotations
from tinydb import TinyDB, Query
from typing import Dict, Any, List, Optional
import os, json, datetime

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
DATA_DIR = os.path.normpath(DATA_DIR)
os.makedirs(DATA_DIR, exist_ok=True)

TESTS_FILE = os.path.join(DATA_DIR, "tests.json")
QUIZ_FILE = os.path.join(DATA_DIR, "quiz_questions.json")
DB_FILE = os.path.join(DATA_DIR, "results_db.json")

def load_tests() -> List[Dict[str, Any]]:
    if not os.path.exists(TESTS_FILE):
        return []
    with open(TESTS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_tests(tests: List[Dict[str, Any]]):
    with open(TESTS_FILE, "w", encoding="utf-8") as f:
        json.dump(tests, f, indent=2, ensure_ascii=False)

def load_quiz_questions() -> List[Dict[str, Any]]:
    if not os.path.exists(QUIZ_FILE):
        return []
    with open(QUIZ_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_quiz_questions(questions: List[Dict[str, Any]]):
    with open(QUIZ_FILE, "w", encoding="utf-8") as f:
        json.dump(questions, f, indent=2, ensure_ascii=False)

def get_db() -> TinyDB:
    return TinyDB(DB_FILE, sort_keys=True, indent=2, separators=(',', ': '))

def log_result(item_name: str, outcome: str, notes: str = "", user: str = "guest") -> int:
    db = get_db()
    return db.table("results").insert({
        "item": item_name,
        "outcome": outcome,
        "notes": notes,
        "user": user,
        "ts": datetime.datetime.now().isoformat(timespec="seconds")
    })

def list_results(user: Optional[str] = None) -> List[Dict[str, Any]]:
    db = get_db()
    t = db.table("results")
    if user:
        Q = Query()
        return t.search(Q.user == user)
    return t.all()

def delete_result(doc_id: int):
    db = get_db()
    db.table("results").remove(doc_ids=[doc_id])
