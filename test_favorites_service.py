# Name: Craig Harker and Sebastian Van Hemelrijck Noya
# Course: CS361 - Software Engineering 1
# Assignment: Assignment 9
# Due Date: 8/10/26
# Description: Tests for the favorites and saved items REST API

import importlib
import time

import pytest

import storage
from app import app


@pytest.fixture()
def client(tmp_path, monkeypatch):
    monkeypatch.setattr(storage, "DATA_FILE", tmp_path / "favorites.json")
    app.config.update(TESTING=True)
    return app.test_client()


def test_save_item_returns_saved_item_as_json(client):
    """A valid item is persisted and returned with service-owned fields."""
    response = client.post("/favorites", json={
        "source": "PrepTrack", "source_id": "kit-1", "name": "First aid kit"
    })

    assert response.status_code == 201
    assert response.json["name"] == "First aid kit"
    assert response.json["id"]
    assert response.json["pinned"] is False


def test_saving_duplicate_item_is_handled(client):
    """Duplicate source/source_id pairs are rejected consistently."""
    payload = {"source": "PrepTrack", "source_id": "kit-1", "name": "Water"}
    assert client.post("/favorites", json=payload).status_code == 201

    response = client.post("/favorites", json=payload)

    assert response.status_code == 409
    assert response.json["error"]["code"] == "DUPLICATE_ITEM"


def test_save_item_missing_required_field_returns_400(client):
    """
    A request missing a required field (name/source_id) should be rejected
    with a 400 rather than saved or causing a server error.
    """
    response = client.post("/favorites", json={"source": "PrepTrack", "name": "Water"})
 
    assert response.status_code == 400
    assert response.json["error"]["code"] == "INVALID_ITEM"
 
 
def test_save_item_non_json_body_returns_400(client):
    """
    A request body that isn't a JSON object at all (e.g. a list, or missing
    entirely) should fail validation cleanly instead of raising an exception.
    """
    response = client.post("/favorites", json=["not", "an", "object"])
 
    assert response.status_code == 400
    assert response.json["error"]["code"] == "INVALID_ITEM"


def test_same_source_id_is_separate_for_each_main_program(client):
    first = {
        "source": "StudyPlanner",
        "source_id": "item-1",
        "name": "Review notes",
    }
    second = {
        "source": "HabitTracker",
        "source_id": "item-1",
        "name": "Morning walk",
    }

    assert client.post("/favorites", json=first).status_code == 201
    assert client.post("/favorites", json=second).status_code == 201
    assert client.get("/favorites?source=StudyPlanner").json["count"] == 1
    assert client.get("/favorites?source=HabitTracker").json["count"] == 1


def test_configured_main_program_origin_is_allowed(client, monkeypatch):
    monkeypatch.setenv(
        "MAIN_PROGRAM_ORIGINS",
        "http://localhost:3000,http://localhost:4173",
    )

    response = client.get("/health", headers={"Origin": "http://localhost:3000"})

    assert response.headers["Access-Control-Allow-Origin"] == "http://localhost:3000"
    assert "DELETE" in response.headers["Access-Control-Allow-Methods"]


def test_reliability_50_items_survive_restart(client, monkeypatch):
    """
    Given 50 saved test items, when the service is restarted and the items
    are requested again, then all 50 items are returned with correct info.
    """
    saved_items = []
    for i in range(50):
        response = client.post("/favorites", json={
            "source": "PrepTrack",
            "source_id": f"item-{i}",
            "name": f"Test Item {i}",
        })
        assert response.status_code == 201
        saved_items.append(response.json)
 
    # reload storage from the saved file like a restarted service would
    monkeypatch.setenv("FAVORITES_DATA_FILE", str(storage.DATA_FILE))
    importlib.reload(storage)
    restarted_client = app.test_client()
    reloaded = restarted_client.get(
        "/favorites?source=PrepTrack&page_size=50"
    ).json["items"]

    assert len(reloaded) == 50
    saved_ids = {item["id"] for item in saved_items}
    reloaded_ids = {item["id"] for item in reloaded}
    assert saved_ids == reloaded_ids
 
    for original in saved_items:
        match = next(item for item in reloaded if item["id"] == original["id"])
        assert match["name"] == original["name"]
        assert match["source_id"] == original["source_id"]
        assert match["pinned"] == original["pinned"]


def test_pin_item_appears_first(client):
    """Pinned items sort ahead of unpinned items."""
    first = client.post("/favorites", json={
        "source": "PrepTrack", "source_id": "1", "name": "Water"
    }).json
    second = client.post("/favorites", json={
        "source": "PrepTrack", "source_id": "2", "name": "Blanket"
    }).json

    assert client.patch(f"/favorites/{second['id']}/pin").status_code == 200
    items = client.get("/favorites?source=PrepTrack").json["items"]

    assert items[0]["id"] == second["id"]
    assert items[1]["id"] == first["id"]


def test_pin_nonexistent_item_returns_404(client):
    """
    Pinning an id that was never saved should return 404, not a 500 or a
    silently-created record.
    """
    response = client.patch("/favorites/does-not-exist/pin")
 
    assert response.status_code == 404
    assert response.json["error"]["code"] == "NOT_FOUND"
 
 
def test_unpin_item(client):
    """
    Sending {"pinned": false} should unpin a previously pinned item, and
    the item should move back below still-pinned items in the list.
    """
    saved = client.post("/favorites", json={
        "source": "PrepTrack", "source_id": "1", "name": "Water"
    }).json
 
    pin_response = client.patch(f"/favorites/{saved['id']}/pin")
    assert pin_response.status_code == 200
    assert pin_response.json["pinned"] is True
 
    unpin_response = client.patch(f"/favorites/{saved['id']}/pin", json={"pinned": False})
    assert unpin_response.status_code == 200
    assert unpin_response.json["pinned"] is False
 
 
def test_pin_with_non_boolean_value_returns_400(client):
    """
    The pinned field must be a boolean - a request sending a string or
    number should be rejected rather than coerced.
    """
    saved = client.post("/favorites", json={
        "source": "PrepTrack", "source_id": "1", "name": "Water"
    }).json
 
    response = client.patch(f"/favorites/{saved['id']}/pin", json={"pinned": "yes"})
 
    assert response.status_code == 400
    assert response.json["error"]["code"] == "INVALID_PIN"
 
 
def test_update_item_editable_fields(client):
    """PATCH /favorites/<id> updates allowed fields and leaves others alone."""
    saved = client.post("/favorites", json={
        "source": "PrepTrack", "source_id": "1", "name": "Water"
    }).json
 
    response = client.patch(f"/favorites/{saved['id']}", json={
        "name": "Bottled Water", "category": "Supplies"
    })
 
    assert response.status_code == 200
    assert response.json["name"] == "Bottled Water"
    assert response.json["category"] == "Supplies"
    assert response.json["source_id"] == "1"  # unrelated field is untouched
    assert response.json["id"] == saved["id"]  # identity is untouched
 
 
def test_update_item_rejects_non_editable_field(client):
    """Attempting to change an identity/audit field like source_id is rejected."""
    saved = client.post("/favorites", json={
        "source": "PrepTrack", "source_id": "1", "name": "Water"
    }).json
 
    response = client.patch(f"/favorites/{saved['id']}", json={"source_id": "hacked"})
 
    assert response.status_code == 400
    assert response.json["error"]["code"] == "INVALID_UPDATE"
 
 
def test_update_nonexistent_item_returns_404(client):
    """Updating an id that was never saved returns 404."""
    response = client.patch("/favorites/does-not-exist", json={"name": "New Name"})
 
    assert response.status_code == 404
    assert response.json["error"]["code"] == "NOT_FOUND"
 
 
def test_update_item_empty_body_returns_400(client):
    """An empty update body is rejected rather than treated as a no-op success."""
    saved = client.post("/favorites", json={
        "source": "PrepTrack", "source_id": "1", "name": "Water"
    }).json
 
    response = client.patch(f"/favorites/{saved['id']}", json={})
 
    assert response.status_code == 400
    assert response.json["error"]["code"] == "INVALID_UPDATE"


def test_update_item_rejects_empty_name(client):
    """A saved item still needs a non-empty name after an update."""
    saved = client.post("/favorites", json={
        "source": "PrepTrack", "source_id": "1", "name": "Water"
    }).json

    response = client.patch(f"/favorites/{saved['id']}", json={"name": ""})

    assert response.status_code == 400
    assert response.json["error"]["code"] == "INVALID_UPDATE"
 
 
def test_delete_item(client):
    """DELETE removes a saved item so it no longer appears in the list."""
    saved = client.post("/favorites", json={
        "source": "PrepTrack", "source_id": "1", "name": "Water"
    }).json
 
    response = client.delete(f"/favorites/{saved['id']}")
    assert response.status_code == 204
 
    items = client.get("/favorites?source=PrepTrack").json["items"]
    assert all(item["id"] != saved["id"] for item in items)
 
 
def test_delete_nonexistent_item_returns_404(client):
    """Deleting an id that was never saved returns 404."""
    response = client.delete("/favorites/does-not-exist")
 
    assert response.status_code == 404
    assert response.json["error"]["code"] == "NOT_FOUND"
 
 
def test_pagination_returns_requested_page_size(client):
    """GET /favorites splits results across pages of the requested size."""
    for i in range(25):
        client.post("/favorites", json={
            "source": "PrepTrack", "source_id": f"page-{i}", "name": f"Item {i}"
        })
 
    first_page = client.get("/favorites?source=PrepTrack&page=1&page_size=10").json
    second_page = client.get("/favorites?source=PrepTrack&page=2&page_size=10").json
    third_page = client.get("/favorites?source=PrepTrack&page=3&page_size=10").json
 
    assert first_page["total"] == 25
    assert len(first_page["items"]) == 10
    assert len(second_page["items"]) == 10
    assert len(third_page["items"]) == 5  # remainder on the last page
 
    # No overlap between pages
    first_ids = {item["id"] for item in first_page["items"]}
    second_ids = {item["id"] for item in second_page["items"]}
    assert first_ids.isdisjoint(second_ids)
 
 
def test_pagination_invalid_page_returns_400(client):
    """A page number below 1 is rejected."""
    response = client.get("/favorites?page=0")
 
    assert response.status_code == 400
    assert response.json["error"]["code"] == "INVALID_PAGE"


def test_performance_100_items_sorted_within_one_second(client):
    """Verify sorted retrieval stays below the one-second requirement."""
    for i in range(100):
        response = client.post("/favorites", json={
            "source": "PrepTrack",
            "source_id": f"perf-{i}",
            "name": f"Perf Item {i}",
        })
        assert response.status_code == 201
        if i % 10 == 0:
            client.patch(f"/favorites/{response.json['id']}/pin")
 
    start = time.perf_counter()
    response = client.get("/favorites?source=PrepTrack&page_size=100")
    elapsed = time.perf_counter() - start
 
    assert response.status_code == 200
    assert elapsed < 1.0
 
    items = response.json["items"]
    assert len(items) == 100
 
    # make sure the pinned items are grouped first too
    pinned_flags = [item["pinned"] for item in items]
    first_unpinned = pinned_flags.index(False)
    assert all(pinned_flags[:first_unpinned])
    assert not any(pinned_flags[first_unpinned:])
