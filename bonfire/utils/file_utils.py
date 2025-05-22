import base64
from typing import Any


def make_json_serializable(obj: Any) -> Any:
    """
    Recursively convert bytes in a structure to base64-encoded strings for JSON serialization.
    """
    if isinstance(obj, dict):
        return {k: make_json_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [make_json_serializable(v) for v in obj]
    elif isinstance(obj, bytes):
        return base64.b64encode(obj).decode("utf-8")
    else:
        return obj
