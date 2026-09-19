"""Stable fingerprints for side effects. Hashing, used for exactly-once."""
import hashlib  # noqa: F401
import json  # noqa: F401
import uuid
from datetime import date


import json

def canonical_json(value) -> str:
    """TODO (Part 2.1): one spelling per meaning.
    Sorted keys, no spaces, and whole floats as integers (12.0 and 12 are the same drive id),
    including inside nested dicts and lists."""
    
    def normalize(val):
        # Convert whole floats to integers
        if isinstance(val, float) and val.is_integer():
            return int(val)
        # Recursively sort keys in dicts
        elif isinstance(val, dict):
            return {k: normalize(val[k]) for k in sorted(val.keys())}
        # Recursively clean up lists
        elif isinstance(val, list):
            return [normalize(item) for item in val]
        return val

    normalized_val = normalize(value)
    # separators=(',', ':') removes spaces between keys and values
    return json.dumps(normalized_val, separators=(',', ':'))



import hashlib

def idempotency_key(run_id: str, seq: int, tool_name: str, args: dict) -> str:
    """Generate a unique SHA-256 hash for a specific tool call execution context."""
    raw_data = canonical_json({"run_id": run_id, "seq": seq, "tool_name": tool_name, "args": args})
    return hashlib.sha256(raw_data.encode("utf-8")).hexdigest()



import hashlib
from datetime import date

def notification_dedupe_key(roll_no: str, message: str, day: date) -> str:
    """Generate a unique key for message logs that strips extra inner and padding spaces."""
    # Split by any whitespace and rejoin with a single space to normalize space groupings
    normalized_message = " ".join(message.split())
    
    # Form the raw tracking base sequence string
    raw_str = f"{roll_no}:{normalized_message}:{day.isoformat()}"
    return hashlib.sha256(raw_str.encode("utf-8")).hexdigest()

