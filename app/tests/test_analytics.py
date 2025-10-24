from datetime import timedelta, datetime


def test_user_ids_by_day(test_client, test_event_data):
    response = test_client.post("/api/v1/event/", json=[test_event_data])
    assert response.status_code == 200

    occurred_date = test_event_data["occurred_at"][:10]

    response = test_client.get(
        "/api/v1/stats/dau",
        params={
            "from": datetime.fromisoformat(occurred_date),
            "to": datetime.fromisoformat(occurred_date) + timedelta(days=1),
        },
    )
    assert response.status_code == 200
    data = response.json()

    assert "user_count" in data
    assert data.get("user_count") == 1


def test_top_events(test_client, test_event_data):
    response = test_client.post("/api/v1/event/", json=[test_event_data])
    assert response.status_code == 200

    occurred_date = test_event_data["occurred_at"][:10]

    response = test_client.get(
        "/api/v1/stats/top-events",
        params={
            "from": datetime.fromisoformat(occurred_date),
            "to": datetime.fromisoformat(occurred_date) + timedelta(days=1),
            "limit": 1,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "count" in data
    assert "response" in data
    assert test_event_data.get("event_type") == data.get("response")[0].get(
        "event_type"
    )


def test_retention_analysis(test_client, test_event_data):
    response = test_client.post("/api/v1/event/", json=[test_event_data])
    assert response.status_code == 200

    occurred_date = test_event_data["occurred_at"][:10]

    response = test_client.get(
        "/api/v1/stats/retention",
        params={
            "start_date": datetime.fromisoformat(occurred_date).date(),
            "window": 7,
            "page_size": 10,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "cursor" in data
    assert "response" in data
    assert len(data.get("response")) >= 1
    assert data.get("response")[0].get("event_id") == test_event_data.get("event_id")
