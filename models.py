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

    """
    pass

def is_duplicate(new_item, existing_items):
    """

    """
    pass
