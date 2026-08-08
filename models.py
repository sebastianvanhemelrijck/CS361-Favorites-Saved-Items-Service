# Contributors: Craig Harker & Sebastian Van Hemelrijck Noya
# Course: CS361 - Software Engineering 1
# Assignment: Assignment 9
# Due Date: 8/10/26
# Description:
    # Defines the shape of a "saved item" and helpers for validating
    # incoming data before it's handed to storage.py.

    # Each item will have the following:
    # - id       (str) assigned by storage.py
    # - pinned   (bool) to determine a favorite, set to False when 1st saved
    # - saved_at (str/float) timestamp, used for sort order for non-pinned items
    # NOTE: We should determine some other factors for item data required (i.e. 
    # name, url, description, etc.)

REQUIRED_FIELDS = []

def validate_new_items(data):
    """
    Validate payload for a new item before saving it.

    TODO:
    - Check 'data' is a dict/JSON object
    - Check that all fields in REQUIRED_FIELDS are present
    - Return (True, None) if valid, or (False, "error message") if not,
      so app.py can decide how to respond (e.g. 400 Bad Request)
    """
    pass

def is_duplicate(new_item, existing_items):
    """
    Determine whether an item is already saved.

    TODO:
    - Decide what makes two items the same (i.e url or unique identifier)
    - Return True if a matching item already exists in existing_items,
      False otherwise
    """
    pass
