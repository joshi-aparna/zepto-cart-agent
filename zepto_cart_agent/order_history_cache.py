import json
import time
from pathlib import Path

CACHE_FILE = Path(__file__).resolve().parent.parent / "order_history_cache.json"
TTL = 900  # 15 minutes

def get_order_history(fetch_history):
    if CACHE_FILE.exists():
        cached = json.loads(CACHE_FILE.read_text())
        if time.time() - cached["fetched_at"] < TTL:
            return cached["response"]

    response = fetch_history()
    CACHE_FILE.write_text(json.dumps({
        "fetched_at": time.time(),
        "response": response,
    }))
    return response