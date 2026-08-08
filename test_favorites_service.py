# Contributors: Craig Harker & Sebastian Van Hemelrijck Noya
# Course: CS361 - Software Engineering 1
# Assignment: Assignment 9
# Due Date: 8/10/26
# Description:
    # Tests for Favorite/Saved Items microservice.
    # Basing our tests off our two user stories.

import time

def test_save_item_returns_saved_item_as_json():
    """
    Given the user selects an item that isn't already saved,
    when the Main Program sends the item to the service,
    then the service saves it and returns the saved item as JSON.
    
    TODO:
    - POST a new item to /favorites
    - Confirm the response status code is 201
    - Confirm the response JSON contains the item data plus an assigned id
    """
    pass

def test_saving_duplicate_item_is_handled():
    """
    Covers the "not already saved" condition of - decide what should happen
    when a duplicate is submitted (either reject or return the existing item,
    we just need to be consistent)

    TODO:
    - Save an item
    - Attempt to save the same item again
    - Assert the expected behavior (e.g. 409 conflict)
    """
    pass

def test_reliability_50_items_survive_restart():
    """
    Given 50 saved test items, when the service is restarted and the
    items are requested again, then all 50 items are returned with the
    correct information.

    TODO:
    - Save 50 test items via POST /favorites
    - Restart the service (this may mean literally stopping and starting
      the flask process, or reloading storage.py's state fresh from
      favorites.json to simluate a restart)
    - Get /favorites and confirm all 50 items are present with correct data
    """
    pass

def test_pin_item_appears_first():
    """
    Given the user has saved items, when the user pins one of them and
    requests the list again, then the pinned item appears before the
    unpinned items.

    TODO:
    - Save a few items
    - Pin one of them vai PATCH /favorites/<id>/pin
    - GET /favorites and confirm the pinned item is first in the list
    """
    pass

def test_performance_100_items_sorted_within_one_second():
    """
    Given a user has 100 saved items, when the Main Program requests
    the list, then the service returns the sorted list within one second.

    TODO:
    - Save 100 test items (pin a few of them)
    - Record start time, call GET /favorites, record end time
    - Confirm (end_time - start_time) < 1.0 second
    - Confirm the returned list is actually sorted correctly
    """
    pass