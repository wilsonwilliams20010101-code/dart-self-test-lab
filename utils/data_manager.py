import os, json, datetime
from tinydb import TinyDB

_DB = None
def get_db():
    global _DB
    if _DB is None:
        os.makedirs("data", exist_ok=True)
        _DB = TinyDB(os.path.join("data", "local_db.json"))
    return _DB

def load_tests():
    path = os.path.join("data", "tests.json")
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_tests(tests):
    with open(os.path.join("data","tests.json"), "w", encoding="utf-8") as f:
        json.dump(tests, f, ensure_ascii=False, indent=2)

def load_quiz_questions():
    path = os.path.join("data","quiz_questions.json")
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_quiz_questions(qs):
    with open(os.path.join("data","quiz_questions.json"), "w", encoding="utf-8") as f:
        json.dump(qs, f, ensure_ascii=False, indent=2)

def log_result(item_name: str, outcome: str, notes: str = "", user: str = "guest", **extra) -> int:
    db = get_db()
    payload = {
        "item": item_name,
        "outcome": outcome,
        "notes": notes,
        "user": user,
        "ts": datetime.datetime.now().isoformat(timespec="seconds")
    }
    payload.update(extra)
    return db.table("results").insert(payload)

def list_results(user: str | None = None):
    rows = get_db().table("results").all()
    if user:
        rows = [r for r in rows if r.get("user")==user]
    return rows