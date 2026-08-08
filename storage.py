# Name: Craig Harker and Sebastian Van Hemelrijck Noya
# Course: CS361 - Software Engineering 1
# Assignment: Assignment 9
# Due Date: 8/10/26
# Description: JSON storage for saved items and favorites

import json
import os
import uuid
from datetime import datetime, timezone
from pathlib import Path

DATA_FILE = Path(
    os.environ.get("FAVORITES_DATA_FILE", Path(__file__).with_name("favorites.json"))
)


def load_items():
    """
    Load every saved item.

    A missing or empty file means nothing has been saved yet. Bad JSON raises an
    error so existing data is not silently replaced.
    """
    if not DATA_FILE.exists() or DATA_FILE.stat().st_size == 0:
        return []
    with DATA_FILE.open("r", encoding="utf-8") as data_file:
        items = json.load(data_file)
    if not isinstance(items, list):
        raise ValueError("favorites data must contain a JSON list")
    return items


def save_items(items):
    """
    Write the full saved item list.

    The new JSON is completed in a temporary file before it replaces the old
    file. This keeps a partial write from damaging the saved list.
    """
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    temp_file = DATA_FILE.with_suffix(DATA_FILE.suffix + ".tmp")
    with temp_file.open("w", encoding="utf-8") as output:
        json.dump(items, output, indent=2)
    os.replace(temp_file, DATA_FILE)


def save_item(item):
    """
    Add service-owned fields and save one item.

    The service creates the id, pin state, and save time even if the request
    sends values with the same names.
    """
    items = load_items()
    saved_item = {
        **item,
        "id": generate_id(),
        "pinned": False,
        "saved_at": datetime.now(timezone.utc).isoformat(),
    }
    items.append(saved_item)
    save_items(items)
    return saved_item


def get_all_items():
    """
    Return favorites first and newer items first inside each group.

    :return: sorted copy of every saved item
    """
    newest_first = sorted(
        load_items(), key=lambda item: item.get("saved_at", ""), reverse=True
    )
    return sorted(newest_first, key=lambda item: not item.get("pinned", False))


def pin_item(item_id, pinned=True):
    """
    Change the favorite state for one saved item.

    :return: updated item or none when the id is unknown
    """
    items = load_items()
    for item in items:
        if item.get("id") == item_id:
            item["pinned"] = bool(pinned)
            save_items(items)
            return item
    return None


def generate_id():
    """Create a unique id owned by the service."""
    return str(uuid.uuid4())
