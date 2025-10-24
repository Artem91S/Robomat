def test_create_event(test_client, test_event_data):
    response = test_client.post("/api/v1/event/", json=[test_event_data])
    assert response.status_code == 200
    data = response.json()

    assert isinstance(data, list)
    assert len(data) == 1
    event = data[0]
    assert event["event_id"] == test_event_data["event_id"]
