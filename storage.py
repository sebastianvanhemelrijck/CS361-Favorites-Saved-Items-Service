# Contributors: Craig Harker & Sebastian Van Hemelrijck Noya
# Course: CS361 - Software Engineering 1
# Assignment: Assignment 9
# Due Date: 8/10/26
# Description:
    # Persistence layer for Favorite/Saved Items microservice.
    # Handles all reading from and writing to favorites.json, so app.py never
    # has to deal with file I/O directly.
    
    # The pattern used here: load the file into memory, modify it, write the
    # whole thing back.

import json
import os
import uuid

DATA_FILE = "favorites.json"

def load_items():
    """
    Load all saved items from favorites.json.

    TODO:
    - If DATA_FILE doesn't exist yet (first run), return an empty list
      (and possibly create the file at that point)
    - Otherwise, open the file and json.load() it, returning the list of items
    - Consider what happens if the file exists but is empty/corrupted
    """
    pass

def save_items(items):
    """
    Persist the full list of items to favorites.json.

    Writes to a temp file first, then replaces the real data
    file with os.replace().

    TODO:
    - Write 'items' as JSON to a temp file (e.g. favorites.json.tmp)
    - Use os.replace() to move temp file over DATA_FILE
    """
    pass

def save_item(item):
    """
    Add a new item to storage and return saved version (with an 
    assigned id, pinned=False default, and a saved_at timestamp).

    TODO:
    - Load existing items via load_items()
    - Generate a unique id for the new item (generate_id() below)
    - Set default fields: "pinned": False, "saved_at": <timestamp>
    - Append the new item to the list
    - Call save_items() to persist
    - Return the newly saved item (as a dict) so app.py can return it as JSON
    """
    pass

def get_all_items():
    """
    Return all saved items, sorted with pinned items first.

    TODO:
    - Load items via load_items()
    - Sort so pinned items come before unpinned items. Within each group,
      a consistent order (e.g. by saved_at) as a default.
      Example:
        sorted(items, key=lambda x: (not x["pinned"], x["saved_at"]))
    - Return the sorted list
    """
    pass

def pin_item(item_id):
    """
    Mark a specific item as pinned.

    TODO:
    - Load items via load_items()
    - Find the item matching item_id
    - If not found, decide how to signal that to app.py (e.g. return None,
      or raise a custom exception, so app.py can return a 404)
    - Set that item's "pinned" field to True
    - Call save_items() to persist the change
    - Return the updated item
    """
    pass

def generate_id():
    """
    Generate a unique identifier for a new item.

    TODO:
    - Use uuid.uuid4() to generate unique identifiers.
    """
    return str(uuid.uuid4())