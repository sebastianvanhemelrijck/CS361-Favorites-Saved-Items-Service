# Name: Craig Harker and Sebastian Van Hemelrijck Noya
# Course: CS361 - Software Engineering 1
# Assignment: Assignment 9
# Due Date: 8/10/26
# Description: Validation helpers for saved item requests

REQUIRED_FIELDS = ["source_id", "name"]


def validate_new_item(data):
    """
    Check and clean one saved item request.

    Main idea:
    - require the fields used to identify and display the item
    - clean the optional text fields
    - return the cleaned item with an error when something is wrong

    :param data: JSON body sent by the Main Program
    :return: normalized item and validation error
    """
    if not isinstance(data, dict):
        return None, "The request body must be a JSON object."

    normalized = dict(data)
    for field in REQUIRED_FIELDS:
        value = normalized.get(field)
        if not isinstance(value, str) or not value.strip():
            return None, f"{field} is required and must be a non-empty string."
        normalized[field] = value.strip()

    normalized["source"] = str(normalized.get("source", "unknown")).strip() or "unknown"
    for field in ("description", "category", "url"):
        value = normalized.get(field, "")
        if value is not None and not isinstance(value, str):
            return None, f"{field} must be a string."
        normalized[field] = (value or "").strip()

    if "metadata" in normalized and not isinstance(normalized["metadata"], dict):
        return None, "metadata must be a JSON object."

    return normalized, None


def is_duplicate(new_item, existing_items):
    """
    Check whether the same Main Program already saved an item.

    :param new_item: normalized item to check
    :param existing_items: items already in storage
    :return: true when source and source_id both match
    """
    source = new_item.get("source", "unknown").casefold()
    source_id = new_item.get("source_id", "")
    return any(
        item.get("source", "unknown").casefold() == source
        and item.get("source_id") == source_id
        for item in existing_items
    )
