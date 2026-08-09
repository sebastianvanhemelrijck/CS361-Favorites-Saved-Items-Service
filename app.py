# Name: Craig Harker and Sebastian Van Hemelrijck Noya
# Course: CS361 - Software Engineering 1
# Assignment: Assignment 9
# Due Date: 8/10/26
# Description: REST API routes for saving items and pinning favorites

import os

from flask import Flask, jsonify, request

from models import is_duplicate, validate_new_item
import storage

app = Flask(__name__)


@app.after_request
def allow_main_program(response):
    """Allow configured browser-based Main Programs to call this API."""
    configured = os.environ.get(
        "MAIN_PROGRAM_ORIGINS",
        os.environ.get(
            "MAIN_PROGRAM_ORIGIN",
            "http://localhost:5173,http://127.0.0.1:5173",
        ),
    )
    allowed = {
        value.strip().rstrip("/") for value in configured.split(",") if value.strip()
    }
    origin = (request.headers.get("Origin") or "").rstrip("/")
    if origin in allowed:
        response.headers["Access-Control-Allow-Origin"] = origin
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "GET,POST,PATCH,OPTIONS"
    return response


@app.get("/health")
def health():
    return jsonify({"service": "favorites", "status": "ok"})


@app.post("/favorites")
def save_favorite():
    """
    Save a new item.

    A saved item starts unpinned. Its source and source_id pair must be unique.
    """
    item, error = validate_new_item(request.get_json(silent=True))
    if error:
        return jsonify({"error": {"code": "INVALID_ITEM", "message": error}}), 400
    if is_duplicate(item, storage.load_items()):
        return jsonify(
            {
                "error": {
                    "code": "DUPLICATE_ITEM",
                    "message": "That item is already saved for this source.",
                }
            }
        ), 409
    return jsonify(storage.save_item(item)), 201


@app.route("/favorites", methods=["GET"])
def get_favorites():
    """
    Return saved items with favorites first.

    The optional source query keeps different Main Programs separate.
    Results are paginated with a default size of 20
    """
    items = storage.get_all_items()
    source = request.args.get("source", "").strip().casefold()
    if source:
        items = [item for item in items if item.get("source", "").casefold() == source]

    page = request.args.get("page", 1, type=int)
    page_size = request.args.get("page_size", 20, type=int)
    if page < 1 or page_size < 1:
        return jsonify(
            {"error": {"code": "INVALID_PAGE", "message": "page and page_size must be positive integers."}}
        ), 400

    total = len(items)
    start = (page - 1) * page_size
    page_items = items[start:start + page_size]

    return jsonify({
        "count": len(page_items),
        "total": total,
        "page": page,
        "page_size": page_size,
        "items": page_items,
    })


@app.route("/favorites/<item_id>/pin", methods=["PATCH"])
def pin_favorite(item_id):
    """
    Change whether a saved item is a favorite.

    The pinned value defaults to true so a request body is optional.
    """
    payload = request.get_json(silent=True) or {}
    pinned = payload.get("pinned", True)
    if not isinstance(pinned, bool):
        return jsonify(
            {
                "error": {
                    "code": "INVALID_PIN",
                    "message": "pinned must be true or false.",
                }
            }
        ), 400
    updated = storage.pin_item(item_id, pinned)
    if updated is None:
        return jsonify(
            {
                "error": {
                    "code": "NOT_FOUND",
                    "message": "The saved item was not found.",
                }
            }
        ), 404
    return jsonify(updated)


@app.route("/favorites/<item_id>", methods=["DELETE"])
def delete_favorite(item_id):
    """Remove a saved item entirely."""
    deleted = storage.delete_item(item_id)
    if not deleted:
        return jsonify(
            {"error": {"code": "NOT_FOUND", "message": "The saved item was not found."}}
        ), 404
    return "", 204


@app.route("/favorites/<item_id>", methods=["PATCH"])
def update_favorite(item_id):
    """Edit one or more fields of a saved item (not source_id, source, or id)."""
    updates, error = validate_update(request.get_json(silent=True))
    if error:
        return jsonify({"error": {"code": "INVALID_UPDATE", "message": error}}), 400
    updated = storage.update_item(item_id, updates)
    if updated is None:
        return jsonify(
            {"error": {"code": "NOT_FOUND", "message": "The saved item was not found."}}
        ), 404
    return jsonify(updated)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=int(os.environ.get("PORT", "5103")), debug=False)
