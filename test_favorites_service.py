# Name: Craig Harker and Sebastian Van Hemelrijck Noya
# Course: CS361 - Software Engineering 1
# Assignment: Assignment 9
# Due Date: 8/10/26
# Description: Tests for the favorites and saved items REST API

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


@pytest.mark.skip(reason="teammate follow-up: add the 50-item restart acceptance test")
def test_reliability_50_items_survive_restart():
    """Verify all saved fields after loading 50 items from a fresh process."""


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


@pytest.mark.skip(reason="teammate follow-up: add the 100-item performance acceptance test")
def test_performance_100_items_sorted_within_one_second():
    """Verify sorted retrieval stays below the one-second requirement."""
