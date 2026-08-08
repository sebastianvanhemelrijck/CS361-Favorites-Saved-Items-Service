# Name: Craig Harker and Sebastian Van Hemelrijck Noya
# Course: CS361 - Software Engineering 1
# Assignment: Assignment 9
# Due Date: 8/10/26
# Description: Tests for the favorites and saved items REST API

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


def test_reliability_50_items_surivive_restart(client):
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
 
    # storage.py keeps no in-memory state - every call reads favorites.json
    # from disk. Calling load_items() again reproduces exactly what a
    # freshly restarted process would see. This exercises the same code
    # path a real restart would.
    reloaded = storage.load_items()
 
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


def test_performance_100_items_sorted_within_one_second():
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
    response = client.get("/favorites?source=PrepTrack")
    elapsed = time.perf_counter() - start
 
    assert response.status_code == 200
    assert elapsed < 1.0
 
    items = response.json["items"]
    assert len(items) == 100
 
    # Confirm the pinned items are actually grouped first, not just fast.
    pinned_flags = [item["pinned"] for item in items]
    first_unpinned = pinned_flags.index(False)
    assert all(pinned_flags[:first_unpinned])
    assert not any(pinned_flags[first_unpinned:])
