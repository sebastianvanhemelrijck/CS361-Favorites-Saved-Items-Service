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

    """
    pass

def save_items(items):
    """
    
    """
    pass

def save_item(item):
    """
    
    """
    pass

def get_all_items():
    """
    
    """
    pass

def pin_item(item_id):
    """
    
    """
    pass

def generate_id():
    """
    
    """
    pass