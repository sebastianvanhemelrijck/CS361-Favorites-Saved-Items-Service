# Favorites and Saved Items Service

MS3 is a reusable service for saving and pinning items from different Main
Programs.

## Communication contract

The service uses a REST API with JSON at `http://127.0.0.1:5103` by default.

| Method and path | Purpose |
| --- | --- |
| `GET /health` | Check whether the service is running |
| `POST /favorites` | Save an item from a Main Program |
| `GET /favorites?source=PrepTrack` | List saved items with pinned items first |
| `PATCH /favorites/{id}/pin` | Pin an item, or send `{"pinned": false}` to unpin it |

New items require `source_id` and `name`. `source`, `description`, `category`,
`url`, and a JSON `metadata` object are optional. Duplicate `source` and
`source_id` pairs return HTTP 409.

```powershell
python -m pip install -r requirements.txt
python app.py
```

In another terminal:

```powershell
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:5103/favorites `
  -ContentType application/json `
  -Body '{"source":"PrepTrack","source_id":"kit-1","name":"First aid kit"}'
```

Run the automated tests with `python -m pytest -q`.

## Sprint 3 stories

- Save an item as a favorite.
- Pin an urgent or important item at the top of the saved-items list.

## Remaining shared work

The required save, list, pin, persistence, validation, and PrepTrack contract
are implemented. Delete/update operations, pagination, and the skipped
50/100-item acceptance tests remain available for another teammate.
