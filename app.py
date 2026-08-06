# Contributors: Craig Harker & Sebastian Van Hemelrijck Noya
# Course: CS361 - Software Engineering 1
# Assignment: Assignment 9
# Due Date: 8/10/26
# Description:
    # Flask entry point for the Favorite/Saved Items microservice.
    # This file defines the HTTP routes the main program will call:
    #   POST  /favorites    -> save a new item as a favorite
    #   GET   /favorites    -> return all saved items (favorites first)
    #   PATCH /favorites    -> mark an existing item as a favorite (not just saved)

    # Route handlers parse the request, call into storage.py to do
    # the actual work, and format the response. Logic such as
    # sorting, persistence, and ID generation will go in storage.py
    # instead of here.

    # Note that a favorite and a saved are different. You can have a list of saved 
    # items but still have favorites within your saved items (not all saved items 
    # are favorites but all favorites are saved).

from flask import Flask, request, jsonify
import storage

app = Flask(__name__)

@app.route("/favorites, methods=["POST"])
def save_favorite():
    """
    Save a new item as a favorite.

    TODO:
    - Get the item data from the incoming request (request.get_json())
    - Validate that required fields are present (decide what an item 
      needs e.g. name, url, etc. Reject with a 400 if invalid)
    - Check if the item is already saved (decide how to detect duplicates)
    - Call storage.save_item(item) to make sure the saved data persists
    - Return the saved item as JSON with a 201 status code
    """
    pass

@app.route("/favorites", methods=["GET"])
def get_favorites():
    """
    Return all saved items, with pinned items appearing before unpinned items

    TODO:
    - Call storage.get_all_items() to load everything from persistence
    - Sort so pinned items come first (we could have storage.py already sort)
    - Return the list as JSON
    """
    pass

@app.route("/favorites/<item_id>/pin", methods=["PATCH"])
def pin_favorite(item_id):
    """
    Mark an existing saved item as a favorite.

    TODO:
    - Call storage.pin_item(item_id) to update the item
    - Handle the case where item_id doesn't exist (return 404)
    - Return the udpated item as JSON
    """
    pass



if __name__ == "__main__":
    app.run(port=5002, debug=True)
